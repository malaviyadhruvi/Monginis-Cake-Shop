from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Ensure profile is created when a new user registers."""
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)
        
        # Generate letter avatar if no profile picture is uploaded
        if not profile.profile_picture:
            generate_letter_avatar(instance.username[0].upper(), instance.username)
            profile.profile_picture = f'profile_pics/{instance.username}.png'
            profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile after changes."""
    instance.profile.save()

def generate_letter_avatar(letter, username):
    """Generate a simple letter-based avatar and save it in media/profile_pics/."""
    img_size = (100, 100)
    background_color = (200, 200, 200)  # Gray background
    text_color = (255, 255, 255)  # White text
    font_size = 50

    img = Image.new("RGB", img_size, background_color)
    draw = ImageDraw.Draw(img)

    # Ensure the directory exists before saving the file
    profile_pic_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
    os.makedirs(profile_pic_dir, exist_ok=True)  # ✅ Auto-create the folder

    # Set font path
    font_path = os.path.join(settings.BASE_DIR, "arial.ttf")  # Ensure the font exists
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Center text
    text_size = draw.textbbox((0, 0), letter, font=font)
    text_position = ((img_size[0] - text_size[2]) // 2, (img_size[1] - text_size[3]) // 2)

    draw.text(text_position, letter, font=font, fill=text_color)

    # Save image to media/profile_pics/
    profile_pic_path = os.path.join(profile_pic_dir, f"{username}.png")
    img.save(profile_pic_path)
