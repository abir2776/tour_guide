import decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TourPlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    max_adults = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    max_children = models.PositiveIntegerField(default=0)
    max_infants = models.PositiveIntegerField(default=0)
    price_adult = models.DecimalField(max_digits=10, decimal_places=2)
    price_child = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_infant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    locations = models.ManyToManyField(Location, related_name="tour_plans")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TourDate(models.Model):
    tour_plan = models.ForeignKey(
        TourPlan, on_delete=models.CASCADE, related_name="tour_dates"
    )
    date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tour_plan", "date")
        ordering = ["date"]

    def __str__(self):
        return f"{self.tour_plan.title} - {self.date}"


class TimeSlot(models.Model):
    tour_date = models.ForeignKey(
        TourDate, on_delete=models.CASCADE, related_name="time_slots"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    available_adults = models.PositiveIntegerField()
    available_children = models.PositiveIntegerField()
    available_infants = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tour_date", "start_time")
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.tour_date} - {self.start_time} to {self.end_time}"

    def has_availability(self, adults, children, infants):
        return (
            self.available_adults >= adults
            and self.available_children >= children
            and self.available_infants >= infants
        )


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    tour_plan = models.ForeignKey(
        TourPlan, on_delete=models.CASCADE, related_name="cart_items"
    )
    time_slot = models.ForeignKey(
        TimeSlot, on_delete=models.CASCADE, related_name="cart_items"
    )
    num_adults = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    num_children = models.PositiveIntegerField(default=0)
    num_infants = models.PositiveIntegerField(default=0)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "tour_plan", "time_slot")

    def __str__(self):
        return f"Cart Item - {self.user.username} - {self.tour_plan.title}"

    def calculate_item_price(self):
        total = (
            self.num_adults * self.tour_plan.price_adult
            + self.num_children * self.tour_plan.price_child
            + self.num_infants * self.tour_plan.price_infant
        )
        return total

    def clean(self):
        if self.num_adults > self.tour_plan.max_adults:
            raise ValidationError(
                f"Number of adults exceeds maximum allowed ({self.tour_plan.max_adults})"
            )
        if self.num_children > self.tour_plan.max_children:
            raise ValidationError(
                f"Number of children exceeds maximum allowed ({self.tour_plan.max_children})"
            )
        if self.num_infants > self.tour_plan.max_infants:
            raise ValidationError(
                f"Number of infants exceeds maximum allowed ({self.tour_plan.max_infants})"
            )

    def save(self, *args, **kwargs):
        if not self.item_price:
            self.item_price = self.calculate_item_price()
        super().save(*args, **kwargs)


class Booking(models.Model):
    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("pending", "Pending"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=decimal.Decimal(0)
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    booked_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username}"


class BookingItem(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="booking_items"
    )
    tour_plan = models.ForeignKey(
        TourPlan, on_delete=models.CASCADE, related_name="booking_items"
    )
    time_slot = models.ForeignKey(
        TimeSlot, on_delete=models.CASCADE, related_name="booking_items"
    )
    num_adults = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    num_children = models.PositiveIntegerField(default=0)
    num_infants = models.PositiveIntegerField(default=0)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking Item - {self.booking.id} - {self.tour_plan.title}"
