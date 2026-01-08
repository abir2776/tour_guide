import decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from core.choices import Status
from core.models import GuestUser, User

USER_TYPE_CHOICES = [
    ("user", "User"),
    ("guest", "Guest"),
]


class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    file = models.FileField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def __str__(self):
        return f"{self.status}"


class TourPlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    max_adults = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_adult = models.DecimalField(max_digits=10, decimal_places=2)
    adult_age_min = models.PositiveIntegerField(default=18)
    adult_age_max = models.PositiveIntegerField(default=99)
    max_children = models.PositiveIntegerField(default=0)
    price_child = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    child_age_min = models.PositiveIntegerField(default=3)
    child_age_max = models.PositiveIntegerField(default=17)
    max_infants = models.PositiveIntegerField(default=0)
    price_infant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    infant_age_min = models.PositiveIntegerField(default=0)
    infant_age_max = models.PositiveIntegerField(default=2)
    max_youth = models.PositiveIntegerField(default=0)
    price_youth = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    youth_age_min = models.PositiveIntegerField(default=18)
    youth_age_max = models.PositiveIntegerField(default=25)
    max_student_eu = models.PositiveIntegerField(default=0)
    price_student_eu = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    student_eu_age_min = models.PositiveIntegerField(default=18)
    student_eu_age_max = models.PositiveIntegerField(default=30)

    locations = models.ManyToManyField(Location, related_name="tour_plans", blank=True)
    images = models.ManyToManyField(Image, related_name="images_tour", blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
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
    available_youth = models.PositiveIntegerField(default=0)
    available_student_eu = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tour_date", "start_time")
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.tour_date} - {self.start_time} to {self.end_time}"

    def has_availability(self, adults, children, infants, youth=0, student_eu=0):
        return (
            self.available_adults >= adults
            and self.available_children >= children
            and self.available_infants >= infants
            and self.available_youth >= youth
            and self.available_student_eu >= student_eu
        )


class CartItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart_items", null=True, blank=True
    )
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
    num_youth = models.PositiveIntegerField(default=0)
    num_student_eu = models.PositiveIntegerField(default=0)
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

    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="user"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_tour_plans",
    )
    guest_user = models.ForeignKey(
        GuestUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="guest_tour_plans",
    )

    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=decimal.Decimal(0)
    )
    traveler_details = models.JSONField(default=[])
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
    num_youth = models.PositiveIntegerField(default=0)
    num_student_eu = models.PositiveIntegerField(default=0)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking Item - {self.booking.id} - {self.tour_plan.title}"
