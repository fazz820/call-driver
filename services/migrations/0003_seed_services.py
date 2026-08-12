from django.db import migrations


def seed_services(apps, schema_editor):
    ServiceCategory = apps.get_model('services', 'ServiceCategory')
    Service = apps.get_model('services', 'Service')

    categories_data = [
        {
            'name': 'Airport & Travel',
            'slug': 'airport-travel',
            'description': 'Reliable airport transfers and travel services',
            'icon': 'airplane',
            'sort_order': 1,
            'services': [
                {
                    'name': 'Airport Pickup & Drop-Off',
                    'slug': 'airport-pickup-dropoff',
                    'description': 'Hassle-free airport transfers. We monitor your flight time to ensure timely pickup and drop-off at any airport terminal.',
                    'base_price': '35.00',
                    'price_per_km': '1.50',
                    'duration_minutes': 45,
                },
                {
                    'name': 'International Airport Transfer',
                    'slug': 'international-airport-transfer',
                    'description': 'Premium transfer service for international airports with meet-and-greet at arrivals hall.',
                    'base_price': '55.00',
                    'price_per_km': '2.00',
                    'duration_minutes': 60,
                },
                {
                    'name': 'Business Class Travel',
                    'slug': 'business-class-travel',
                    'description': 'Executive airport transfers in luxury vehicles with complimentary Wi-Fi and refreshments.',
                    'base_price': '75.00',
                    'price_per_km': '2.50',
                    'duration_minutes': 45,
                },
            ],
        },
        {
            'name': 'Night Life',
            'slug': 'night-life',
            'description': 'Safe rides home from bars, clubs, and events',
            'icon': 'moon-stars',
            'sort_order': 2,
            'services': [
                {
                    'name': 'Bar & Night-Out Pickups',
                    'slug': 'bar-night-out-pickups',
                    'description': 'Safe and reliable rides home from bars, pubs, and nightclubs. Don\'t drink and drive — let us take you home.',
                    'base_price': '15.00',
                    'price_per_km': '1.20',
                    'duration_minutes': 20,
                },
                {
                    'name': 'Club VIP Drop-Off',
                    'slug': 'club-vip-dropoff',
                    'description': 'Arrive in style at nightclubs and VIP events. Premium vehicles with professional chauffeurs.',
                    'base_price': '40.00',
                    'price_per_km': '2.00',
                    'duration_minutes': 30,
                },
                {
                    'name': 'Late Night Safe Ride',
                    'slug': 'late-night-safe-ride',
                    'description': '24/7 late-night safety service. Female drivers available upon request for added comfort and security.',
                    'base_price': '20.00',
                    'price_per_km': '1.50',
                    'duration_minutes': 25,
                },
            ],
        },
        {
            'name': 'Medical Transportation',
            'slug': 'medical-transportation',
            'description': 'Compassionate medical transport services',
            'icon': 'heart-pulse',
            'sort_order': 3,
            'services': [
                {
                    'name': 'Patient Pickup & Drop-Off',
                    'slug': 'patient-pickup-dropoff',
                    'description': 'Comfortable and careful transport for patients to and from medical appointments, hospitals, and clinics.',
                    'base_price': '25.00',
                    'price_per_km': '1.50',
                    'duration_minutes': 30,
                },
                {
                    'name': 'Wheelchair-Accessible Transport',
                    'slug': 'wheelchair-accessible-transport',
                    'description': 'Fully wheelchair-accessible vehicles with trained drivers for safe and dignified medical transportation.',
                    'base_price': '35.00',
                    'price_per_km': '1.80',
                    'duration_minutes': 35,
                },
                {
                    'name': 'Senior Care Transport',
                    'slug': 'senior-care-transport',
                    'description': 'Door-through-door service for elderly passengers. Drivers assist with mobility aids, bags, and escorting to appointments.',
                    'base_price': '30.00',
                    'price_per_km': '1.50',
                    'duration_minutes': 35,
                },
                {
                    'name': 'Pharmacy & Prescription Pickup',
                    'slug': 'pharmacy-prescription-pickup',
                    'description': 'We pick up and deliver your prescriptions and medical supplies directly to your home.',
                    'base_price': '12.00',
                    'price_per_km': '1.00',
                    'duration_minutes': 20,
                },
            ],
        },
        {
            'name': 'Special Events',
            'slug': 'special-events',
            'description': 'Professional transportation for your most memorable moments',
            'icon': 'stars',
            'sort_order': 4,
            'services': [
                {
                    'name': 'Wedding Services',
                    'slug': 'wedding-services',
                    'description': 'Make your wedding day magical with our luxury fleet. Elegant vehicles for the bride, groom, and wedding party. Decoration options available.',
                    'base_price': '120.00',
                    'price_per_km': '3.00',
                    'duration_minutes': 120,
                },
                {
                    'name': 'Birthday Party Transport',
                    'slug': 'birthday-party-transport',
                    'description': 'Celebrate in style! Group transport for birthday parties with flexible scheduling and multiple stops.',
                    'base_price': '50.00',
                    'price_per_km': '2.00',
                    'duration_minutes': 60,
                },
                {
                    'name': 'Concert & Event Shuttle',
                    'slug': 'concert-event-shuttle',
                    'description': 'Group transport to concerts, festivals, and sporting events. Pre-book your round trip and avoid traffic.',
                    'base_price': '40.00',
                    'price_per_km': '1.80',
                    'duration_minutes': 45,
                },
                {
                    'name': 'Graduation Day Transport',
                    'slug': 'graduation-day-transport',
                    'description': 'Celebrate your achievement with premium transport for you and your family to the ceremony.',
                    'base_price': '45.00',
                    'price_per_km': '2.00',
                    'duration_minutes': 40,
                },
            ],
        },
        {
            'name': 'Corporate & Business',
            'slug': 'corporate-business',
            'description': 'Executive transport solutions for professionals',
            'icon': 'briefcase',
            'sort_order': 5,
            'services': [
                {
                    'name': 'Corporate Travel',
                    'slug': 'corporate-travel',
                    'description': 'Executive transport for business meetings, conferences, and corporate events. Available on monthly billing.',
                    'base_price': '40.00',
                    'price_per_km': '2.00',
                    'duration_minutes': 30,
                },
                {
                    'name': 'Meeting Point Transfer',
                    'slug': 'meeting-point-transfer',
                    'description': 'Timely transfers between office locations, meeting venues, and client sites. Invoice-based corporate billing.',
                    'base_price': '30.00',
                    'price_per_km': '1.50',
                    'duration_minutes': 25,
                },
                {
                    'name': 'VIP Client Transport',
                    'slug': 'vip-client-transport',
                    'description': 'Impression-making luxury transport for client pickups, site visits, and business entertainment.',
                    'base_price': '65.00',
                    'price_per_km': '2.50',
                    'duration_minutes': 40,
                },
                {
                    'name': 'Staff Shift Transport',
                    'slug': 'staff-shift-transport',
                    'description': 'Reliable employee transportation for shift changes, early mornings, and late-night work. Group booking discounts available.',
                    'base_price': '25.00',
                    'price_per_km': '1.20',
                    'duration_minutes': 35,
                },
            ],
        },
        {
            'name': 'Daily Commute',
            'slug': 'daily-commute',
            'description': 'Regular transportation for your daily routine',
            'icon': 'arrow-repeat',
            'sort_order': 6,
            'services': [
                {
                    'name': 'School Run Service',
                    'slug': 'school-run-service',
                    'description': 'Safe and punctual transportation for children to and from school. GPS-tracked rides with driver background checks.',
                    'base_price': '18.00',
                    'price_per_km': '1.00',
                    'duration_minutes': 25,
                },
                {
                    'name': 'Work Commute',
                    'slug': 'work-commute',
                    'description': 'Daily commute to and from work. Subscribe for weekly or monthly plans and save up to 20%.',
                    'base_price': '15.00',
                    'price_per_km': '1.00',
                    'duration_minutes': 25,
                },
                {
                    'name': 'Grocery & Shopping Trips',
                    'slug': 'grocery-shopping-trips',
                    'description': 'Transport to supermarkets and shopping malls. Drivers can assist with carrying bags to your door.',
                    'base_price': '12.00',
                    'price_per_km': '1.00',
                    'duration_minutes': 20,
                },
            ],
        },
        {
            'name': 'Long Distance & Outstation',
            'slug': 'long-distance-outstation',
            'description': 'Intercity and outstation travel made comfortable',
            'icon': 'signpost-2',
            'sort_order': 7,
            'services': [
                {
                    'name': 'Intercity Transfer',
                    'slug': 'intercity-transfer',
                    'description': 'Comfortable travel between cities. Spacious vehicles with entertainment systems and refreshment stops.',
                    'base_price': '80.00',
                    'price_per_km': '1.20',
                    'duration_minutes': 180,
                },
                {
                    'name': 'Outstation Trip',
                    'slug': 'outstation-trip',
                    'description': 'Multi-day outstation trips with a dedicated driver. Perfect for weekend getaways and business tours.',
                    'base_price': '150.00',
                    'price_per_km': '1.00',
                    'duration_minutes': 480,
                },
                {
                    'name': 'Group Tour Transport',
                    'slug': 'group-tour-transport',
                    'description': 'Minibus and SUV transportation for group trips, sightseeing tours, and family outings.',
                    'base_price': '100.00',
                    'price_per_km': '1.50',
                    'duration_minutes': 240,
                },
            ],
        },
        {
            'name': 'Luxury & VIP',
            'slug': 'luxury-vip',
            'description': 'Premium transportation for discerning clients',
            'icon': 'gem',
            'sort_order': 8,
            'services': [
                {
                    'name': 'Luxury Car Service',
                    'slug': 'luxury-car-service',
                    'description': 'Travel in premium vehicles including Mercedes-Benz, BMW, and Audi. Professional chauffeurs in formal attire.',
                    'base_price': '60.00',
                    'price_per_km': '3.00',
                    'duration_minutes': 30,
                },
                {
                    'name': 'Champagne Package',
                    'slug': 'champagne-package',
                    'description': 'Ultimate luxury experience with complimentary champagne, premium sound system, and ambient lighting.',
                    'base_price': '100.00',
                    'price_per_km': '3.50',
                    'duration_minutes': 45,
                },
                {
                    'name': 'Personal Chauffeur (Hourly)',
                    'slug': 'personal-chauffeur-hourly',
                    'description': 'Your personal chauffeur for the day. Run errands, attend meetings, or explore the city at your own pace.',
                    'base_price': '50.00',
                    'price_per_km': '0.00',
                    'duration_minutes': 60,
                },
            ],
        },
        {
            'name': 'Errands & Delivery',
            'slug': 'errands-delivery',
            'description': 'We handle the deliveries so you don\'t have to',
            'icon': 'box',
            'sort_order': 9,
            'services': [
                {
                    'name': 'Package Delivery',
                    'slug': 'package-delivery',
                    'description': 'Fast and secure same-day package delivery within the city. Real-time tracking and delivery confirmation.',
                    'base_price': '10.00',
                    'price_per_km': '1.00',
                    'duration_minutes': 20,
                },
                {
                    'name': 'Food & Grocery Delivery',
                    'slug': 'food-grocery-delivery',
                    'description': 'Order pickup and delivery from restaurants and grocery stores. Temperature-controlled transport available.',
                    'base_price': '8.00',
                    'price_per_km': '0.80',
                    'duration_minutes': 15,
                },
                {
                    'name': 'Document Courier',
                    'slug': 'document-courier',
                    'description': 'Secure and prompt document delivery for legal, business, and personal needs. Signed delivery confirmation included.',
                    'base_price': '12.00',
                    'price_per_km': '1.00',
                    'duration_minutes': 20,
                },
            ],
        },
        {
            'name': 'Hourly Rentals',
            'slug': 'hourly-rentals',
            'description': 'Flexible hourly transportation for any need',
            'icon': 'clock',
            'sort_order': 10,
            'services': [
                {
                    'name': 'Hourly Car Rental with Driver',
                    'slug': 'hourly-car-rental-driver',
                    'description': 'Rent a vehicle with a driver by the hour. Perfect for multiple errands, appointments, or exploring the city.',
                    'base_price': '25.00',
                    'price_per_km': '0.00',
                    'duration_minutes': 60,
                },
                {
                    'name': 'Half-Day Rental',
                    'slug': 'half-day-rental',
                    'description': 'Four hours of dedicated service with a driver. Ideal for shopping trips, airport runs, or half-day excursions.',
                    'base_price': '80.00',
                    'price_per_km': '0.00',
                    'duration_minutes': 240,
                },
                {
                    'name': 'Full-Day Rental',
                    'slug': 'full-day-rental',
                    'description': 'Eight hours of uninterrupted service. Best value for full-day events, road trips, and corporate days.',
                    'base_price': '140.00',
                    'price_per_km': '0.00',
                    'duration_minutes': 480,
                },
            ],
        },
    ]

    for cat_data in categories_data:
        services_list = cat_data.pop('services')
        category, _ = ServiceCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data,
        )
        for svc_data in services_list:
            Service.objects.get_or_create(
                slug=svc_data['slug'],
                defaults={**svc_data, 'category': category},
            )


def reverse_seed(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    ServiceCategory = apps.get_model('services', 'ServiceCategory')

    slugs = [
        'airport-pickup-dropoff', 'international-airport-transfer', 'business-class-travel',
        'bar-night-out-pickups', 'club-vip-dropoff', 'late-night-safe-ride',
        'patient-pickup-dropoff', 'wheelchair-accessible-transport', 'senior-care-transport',
        'pharmacy-prescription-pickup',
        'wedding-services', 'birthday-party-transport', 'concert-event-shuttle', 'graduation-day-transport',
        'corporate-travel', 'meeting-point-transfer', 'vip-client-transport', 'staff-shift-transport',
        'school-run-service', 'work-commute', 'grocery-shopping-trips',
        'intercity-transfer', 'outstation-trip', 'group-tour-transport',
        'luxury-car-service', 'champagne-package', 'personal-chauffeur-hourly',
        'package-delivery', 'food-grocery-delivery', 'document-courier',
        'hourly-car-rental-driver', 'half-day-rental', 'full-day-rental',
    ]
    Service.objects.filter(slug__in=slugs).delete()

    category_slugs = [
        'airport-travel', 'night-life', 'medical-transportation', 'special-events',
        'corporate-business', 'daily-commute', 'long-distance-outstation',
        'luxury-vip', 'errands-delivery', 'hourly-rentals',
    ]
    ServiceCategory.objects.filter(slug__in=category_slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_alter_service_is_active_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_services, reverse_seed),
    ]
