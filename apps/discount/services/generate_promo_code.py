from random import choices
from string import digits, ascii_lowercase, ascii_uppercase

characters_pull = digits + ascii_lowercase + ascii_uppercase

class PromoCodeGenerator:

    def __init__(self):
        self.generated_promo_code = self.generate_promo_code()

    @staticmethod
    def generate_promo_code(length :int = 20) -> str:
        return ''.join(choices(characters_pull, k=length))

    def check_if_exist_promo_code(self) -> bool:
        from apps.discount.models import PromoCode

        return PromoCode.objects.filter(code=self.generated_promo_code).exists()

    def create_promo_code(self):
        from apps.discount.models import PromoCode

        while self.check_if_exist_promo_code():
            self.generated_promo_code = self.generate_promo_code()
        PromoCode.objects.create(code=self.generated_promo_code)
        return self.generated_promo_code

