from django.contrib import admin

from .models import (
    Booking,
    BookingItem,
    CartItem,
    Image,
    Location,
    Notice,
    TimeSlot,
    TourDate,
    TourPlan,
)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


class TourDateInline(admin.TabularInline):
    model = TourDate
    extra = 1
    fields = ["date", "is_active"]


@admin.register(TourPlan)
class TourPlanAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "max_adults",
        "max_children",
        "max_infants",
        "price_adult",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["title", "description"]
    filter_horizontal = ["locations"]
    inlines = [TourDateInline]


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1
    fields = [
        "start_time",
        "end_time",
        "available_adults",
        "available_children",
        "available_infants",
        "is_active",
    ]


@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ["tour_plan", "date", "is_active", "created_at"]
    list_filter = ["is_active", "date", "tour_plan"]
    search_fields = ["tour_plan__title"]
    inlines = [TimeSlotInline]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = [
        "tour_date",
        "start_time",
        "end_time",
        "available_adults",
        "available_children",
        "available_infants",
        "is_active",
    ]
    list_filter = ["is_active", "tour_date__date"]
    search_fields = ["tour_date__tour_plan__title"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "tour_plan",
        "time_slot",
        "num_adults",
        "num_children",
        "num_infants",
        "item_price",
        "created_at",
    ]
    list_filter = ["created_at", "tour_plan"]
    search_fields = ["user__username", "user__email", "tour_plan__title"]
    readonly_fields = ["item_price", "created_at", "updated_at"]


class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 0
    fields = [
        "tour_plan",
        "time_slot",
        "num_adults",
        "num_children",
        "num_infants",
        "item_price",
    ]
    readonly_fields = [
        "tour_plan",
        "time_slot",
        "num_adults",
        "num_children",
        "num_infants",
        "item_price",
    ]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "total_price",
        "status",
        "booked_by_admin",
        "created_at",
    ]
    list_filter = ["status", "booked_by_admin", "created_at"]
    search_fields = ["user__username", "user__email"]
    readonly_fields = ["total_price", "created_at", "updated_at"]
    inlines = [BookingItemInline]

    fieldsets = (
        (
            "Booking Information",
            {"fields": ("user", "total_price", "status", "booked_by_admin")},
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = [
        "booking",
        "tour_plan",
        "time_slot",
        "num_adults",
        "num_children",
        "num_infants",
        "item_price",
        "created_at",
    ]
    list_filter = ["created_at", "tour_plan"]
    search_fields = ["booking__user__username", "tour_plan__title"]
    readonly_fields = ["created_at"]


admin.site.register(Image)
admin.site.register(Notice)
