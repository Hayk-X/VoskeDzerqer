from django.core.management.base import BaseCommand
from voske_dzerq.models import MenuItem


class Command(BaseCommand):
    help = 'Заполняет базу данных меню ресторана'

    def handle(self, *args, **options):
        menu_items = [
            # ՇԱՈՒՐՄԱ (Shawarma)
            {'name': 'Խոզի մեծ', 'price': 1500, 'category': 'ШАУРМА', 'description': 'հաց,լավաշ'},
            {'name': 'Խոզի փոքր', 'price': 1000, 'category': 'ШАУРМА', 'description': 'հաց,լավաշ'},
            {'name': 'Լոշիկով', 'price': 1200, 'category': 'ШАУРМА', 'description': 'լավաշով'},
            {'name': 'Հավի մեծ', 'price': 1200, 'category': 'ШАУРМА', 'description': 'հաց,լավաշ'},
            {'name': 'Հավի փոքր', 'price': 800, 'category': 'ШАУРМА', 'description': 'հաց,լավաշ'},
            {'name': 'Ղարս խոզի', 'price': 1300, 'category': 'ШАУРМА', 'description': 'հացով'},
            {'name': 'Ղարս հավի', 'price': 1100, 'category': 'ШАУРМА', 'description': 'հացով'},
            {'name': 'Բուրգեր-շաուրմա հավի', 'price': 1200, 'category': 'ШАУРМА', 'description': ''},
            {'name': 'Բուրգեր-շաուրմա խոզի', 'price': 1400, 'category': 'ШАУРМА', 'description': ''},
            {'name': 'Հոթ-Դոգ', 'price': 600, 'category': 'ШАУРМА', 'description': ''},
            {'name': 'Հոթ-Դոգ-XXL', 'price': 800, 'category': 'ШАУРМА', 'description': ''},
            
            # ՄԱՆՂԱԼ (Mangal/Grill)
            {'name': 'Խոզի փափուկ', 'price': 1800, 'category': 'НА МАНГАЛЕ', 'description': '600գ'},
            {'name': 'Խոզի մատ', 'price': 1500, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Խոզի չալաղաջ', 'price': 1400, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Ամբողջական հավ', 'price': 3800, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Տավարի քաբաբ', 'price': 2000, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Հավի քաբաբ', 'price': 1200, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Հավի քաբաբ պանրով', 'price': 1400, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Ծովախեցգետնի քաբաբ', 'price': 2500, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Հորթի Իքի-Բիր', 'price': 2200, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Գառան Իքի-Բիր', 'price': 2100, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Խոզի Իքի-Բիր', 'price': 1800, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Հավի Իքի-Բիր', 'price': 1400, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Շիշ-Թաուկ', 'price': 1300, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Խորոված Կարտոֆիլ', 'price': 800, 'category': 'НА МАНГАЛЕ', 'description': ''},
            {'name': 'Կարտոֆիլ ճմուռ', 'price': 700, 'category': 'НА МАНГАЛЕ', 'description': ''},
            
            # ԼԱՀՄԱՋՈ (Lahmacun)
            {'name': 'Կլասիկ', 'price': 300, 'category': 'ЛАХМАДЖО', 'description': ''},
            {'name': 'Պանրով և մսով', 'price': 400, 'category': 'ЛАХМАДЖО', 'description': ''},
            {'name': 'Սնկով և մսով', 'price': 450, 'category': 'ЛАХМАДЖО', 'description': ''},
            {'name': 'Սունկ,պանիր,միս', 'price': 500, 'category': 'ЛАХМАДЖО', 'description': ''},
            
            # ՖԱԼԱՖԵԼ (Falafel)
            {'name': 'Լոշիկով', 'price': 800, 'category': 'ФАЛАФЕЛ', 'description': ''},
            {'name': 'Լավաշով', 'price': 800, 'category': 'ФАЛАФЕЛ', 'description': ''},
            {'name': 'Հացով', 'price': 700, 'category': 'ФАЛАФЕЛ', 'description': ''},
            {'name': 'Լոշիկով և պանրով', 'price': 1000, 'category': 'ФАЛАФЕЛ', 'description': ''},
            {'name': 'Լավաշով և պանրով', 'price': 1000, 'category': 'ФАЛАФЕЛ', 'description': ''},
            {'name': 'Հատիկով', 'price': 200, 'category': 'ФАЛАФЕЛ', 'description': ''},
            
            # ԱՊՈՒՐՆԵՐ (Soups)
            {'name': 'Բորշչ', 'price': 1400, 'category': 'СУПЫ', 'description': ''},
            {'name': 'Փիթի', 'price': 1300, 'category': 'СУПЫ', 'description': ''},
            {'name': 'Հավապուր', 'price': 1200, 'category': 'СУПЫ', 'description': ''},
            {'name': 'Սոուս տավարի մսով', 'price': 1300, 'category': 'СУПЫ', 'description': ''},
            {'name': 'Հարիսա', 'price': 1100, 'category': 'СУПЫ', 'description': ''},
            
            # ԽՈՐՏԻԿՆԵՐ (Snacks)
            {'name': 'Ֆրի', 'price': 500, 'category': 'ЗАКУСКИ', 'description': ''},
            {'name': 'Գյուղական ֆրի', 'price': 700, 'category': 'ЗАКУСКИ', 'description': ''},
            {'name': 'Հավի թևիկներ', 'price': 1200, 'category': 'ЗАКУСКИ', 'description': ''},
            {'name': 'Նագեթս', 'price': 900, 'category': 'ЗАКУСКИ', 'description': ''},
            
            # ԸՄՊԵԼԻՔՆԵՐ (Drinks)
            {'name': 'Կոկա կոլա 0.5լ', 'price': 400, 'category': 'НАПИТКИ', 'description': '0.5L'},
            {'name': 'Ֆանտա 0.5լ', 'price': 250, 'category': 'НАПИТКИ', 'description': '0.5L'},
            {'name': 'Բնական հյութ', 'price': 400, 'category': 'НАПИТКИ', 'description': ''},
            {'name': 'Լիմոնադ', 'price': 250, 'category': 'НАПИТКИ', 'description': '0.5L'},
            {'name': 'Կվաս', 'price': 350, 'category': 'НАПИТКИ', 'description': '0.5L'},
            {'name': 'Գազավորված ջուր', 'price': 250, 'category': 'НАПИТКИ', 'description': '0.5L'},
            {'name': 'Ջուր', 'price': 200, 'category': 'НАПИТКИ', 'description': '0.5L'},
            {'name': 'Տոմատի հյութ', 'price': 300, 'category': 'НАПИТКИ', 'description': '0.25L'},
            {'name': 'Թան', 'price': 300, 'category': 'НАПИТКИ', 'description': '0.5L'},
            {'name': 'Թան Ֆիրմային', 'price': 300, 'category': 'НАПИТКИ', 'description': '0.3L'},
            {'name': 'Մածնաբրդոշ', 'price': 350, 'category': 'НАПИТКИ', 'description': '0.5L'},
        ]
        
        created_count = 0
        updated_count = 0
        
        for item_data in menu_items:
            menu_item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'price': item_data['price'],
                    'category': item_data['category'],
                    'description': item_data.get('description', ''),
                    'is_available': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Создан: {item_data["name"]} - {item_data["price"]} ֏')
                )
            else:
                # Обновляем существующий элемент, если он изменился
                updated = False
                if menu_item.price != item_data['price']:
                    menu_item.price = item_data['price']
                    updated = True
                if menu_item.category != item_data['category']:
                    menu_item.category = item_data['category']
                    updated = True
                if menu_item.description != item_data.get('description', ''):
                    menu_item.description = item_data.get('description', '')
                    updated = True
                
                if updated:
                    menu_item.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'↻ Обновлен: {item_data["name"]}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Готово! Создано: {created_count}, Обновлено: {updated_count}, Всего: {MenuItem.objects.count()}'
            )
        )

