"""
Thumbnail Generator - Tạo thumbnail cho video YouTube
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Optional, Tuple
from loguru import logger
import textwrap


class ThumbnailGenerator:
    """Tạo thumbnail tự động cho video YouTube"""
    
    # YouTube thumbnail size
    WIDTH = 1280
    HEIGHT = 720
    
    # Colors - TOEIC theme
    BACKGROUND_COLOR = (41, 128, 185)  # Blue
    TEXT_COLOR = (255, 255, 255)  # White
    ACCENT_COLOR = (231, 76, 60)  # Red
    BORDER_COLOR = (52, 73, 94)  # Dark blue
    
    def __init__(self, output_dir: str = "data/thumbnails"):
        """
        Initialize thumbnail generator
        
        Args:
            output_dir: Thư mục lưu thumbnails
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Try to load fonts
        self.title_font = self._load_font(size=80, bold=True)
        self.subtitle_font = self._load_font(size=50)
        self.emoji_font = self._load_font(size=100)
    
    def _load_font(self, size: int = 40, bold: bool = False) -> ImageFont.FreeTypeFont:
        """Load font với fallback"""
        font_paths = [
            # Vietnamese fonts
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            # Common Linux fonts
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            # Ubuntu fonts
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        ]
        
        # Try each font
        for font_path in font_paths:
            try:
                if Path(font_path).exists():
                    return ImageFont.truetype(font_path, size)
            except Exception:
                continue
        
        # Fallback to default
        logger.warning(f"Could not load custom font, using default")
        return ImageFont.load_default()
    
    def create_thumbnail(
        self, 
        title: str, 
        video_name: str,
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Tạo thumbnail cho video
        
        Args:
            title: Title của video (có thể có emoji)
            video_name: Tên file video (để đặt tên thumbnail)
            output_filename: Tên file output (optional)
        
        Returns:
            Path đến thumbnail đã tạo
        """
        try:
            logger.info(f"Creating thumbnail for: {video_name}")
            
            # Create image
            img = Image.new('RGB', (self.WIDTH, self.HEIGHT), self.BACKGROUND_COLOR)
            draw = ImageDraw.Draw(img)
            
            # Add gradient effect (darker at bottom)
            self._add_gradient(img)
            
            # Add border
            self._add_border(draw)
            
            # Parse title and emoji
            clean_title, emojis = self._extract_emojis(title)
            
            # Add main title
            self._add_title(draw, clean_title)
            
            # Add decorative elements
            self._add_decorations(draw)
            
            # Add "TOEIC PART 3" badge if in title
            if "TOEIC" in title.upper():
                self._add_toeic_badge(draw)
            
            # Save thumbnail
            if output_filename:
                filename = output_filename
            else:
                filename = f"{Path(video_name).stem}_thumbnail.jpg"
            
            output_path = self.output_dir / filename
            img.save(output_path, quality=95, optimize=True)
            
            logger.success(f"✅ Thumbnail created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error creating thumbnail: {e}")
            raise
    
    def _add_gradient(self, img: Image.Image):
        """Thêm gradient effect (tối dần ở dưới)"""
        gradient = Image.new('RGBA', (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(gradient)
        
        # Draw gradient from top to bottom
        for y in range(self.HEIGHT):
            alpha = int(255 * (y / self.HEIGHT) * 0.3)  # 30% opacity at bottom
            draw.rectangle([(0, y), (self.WIDTH, y + 1)], fill=(0, 0, 0, alpha))
        
        img.paste(gradient, (0, 0), gradient)
    
    def _add_border(self, draw: ImageDraw.Draw):
        """Thêm border"""
        border_width = 15
        draw.rectangle(
            [(border_width, border_width), 
             (self.WIDTH - border_width, self.HEIGHT - border_width)],
            outline=self.BORDER_COLOR,
            width=border_width
        )
    
    def _extract_emojis(self, text: str) -> Tuple[str, list]:
        """Tách emoji khỏi text"""
        import re
        
        # Regex cho emoji
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", 
            flags=re.UNICODE
        )
        
        emojis = emoji_pattern.findall(text)
        clean_text = emoji_pattern.sub('', text).strip()
        
        return clean_text, emojis
    
    def _add_title(self, draw: ImageDraw.Draw, title: str):
        """Thêm title (wrap text nếu quá dài)"""
        # Remove [TOEIC PART 3] prefix if exists
        title = title.replace("[TOEIC PART 3]", "").strip()
        title = title.replace("🔥", "").strip()
        
        # Wrap text
        max_chars_per_line = 25
        lines = textwrap.wrap(title, width=max_chars_per_line)
        
        # Limit to 3 lines
        if len(lines) > 3:
            lines = lines[:3]
            lines[-1] = lines[-1][:max_chars_per_line-3] + "..."
        
        # Calculate total height
        line_height = 100
        total_height = len(lines) * line_height
        
        # Starting Y position (center vertically)
        y = (self.HEIGHT - total_height) // 2
        
        # Draw each line
        for line in lines:
            # Get text size
            bbox = draw.textbbox((0, 0), line, font=self.title_font)
            text_width = bbox[2] - bbox[0]
            
            # Center horizontally
            x = (self.WIDTH - text_width) // 2
            
            # Draw shadow
            shadow_offset = 4
            draw.text(
                (x + shadow_offset, y + shadow_offset), 
                line, 
                font=self.title_font, 
                fill=(0, 0, 0, 128)
            )
            
            # Draw text
            draw.text((x, y), line, font=self.title_font, fill=self.TEXT_COLOR)
            
            y += line_height
    
    def _add_decorations(self, draw: ImageDraw.Draw):
        """Thêm các decoration (góc, line, etc.)"""
        margin = 60
        corner_length = 80
        line_width = 8
        
        # Top left corner
        draw.line(
            [(margin, margin), (margin + corner_length, margin)], 
            fill=self.ACCENT_COLOR, 
            width=line_width
        )
        draw.line(
            [(margin, margin), (margin, margin + corner_length)], 
            fill=self.ACCENT_COLOR, 
            width=line_width
        )
        
        # Top right corner
        draw.line(
            [(self.WIDTH - margin, margin), (self.WIDTH - margin - corner_length, margin)], 
            fill=self.ACCENT_COLOR, 
            width=line_width
        )
        draw.line(
            [(self.WIDTH - margin, margin), (self.WIDTH - margin, margin + corner_length)], 
            fill=self.ACCENT_COLOR, 
            width=line_width
        )
        
        # Bottom left corner
        draw.line(
            [(margin, self.HEIGHT - margin), (margin + corner_length, self.HEIGHT - margin)], 
            fill=self.ACCENT_COLOR, 
            width=line_width
        )
        draw.line(
            [(margin, self.HEIGHT - margin), (margin, self.HEIGHT - margin - corner_length)], 
            fill=self.ACCENT_COLOR, 
            width=line_width
        )
        
        # Bottom right corner
        draw.line(
            [(self.WIDTH - margin, self.HEIGHT - margin), 
             (self.WIDTH - margin - corner_length, self.HEIGHT - margin)], 
            fill=self.ACCENT_COLOR, 
            width=line_width
        )
        draw.line(
            [(self.WIDTH - margin, self.HEIGHT - margin), 
             (self.WIDTH - margin, self.HEIGHT - margin - corner_length)], 
            fill=self.ACCENT_COLOR, 
            width=line_width
        )
    
    def _add_toeic_badge(self, draw: ImageDraw.Draw):
        """Thêm badge TOEIC PART 3 ở góc trên"""
        badge_text = "TOEIC PART 3"
        badge_width = 400
        badge_height = 80
        badge_x = (self.WIDTH - badge_width) // 2
        badge_y = 50
        
        # Draw badge background
        draw.rounded_rectangle(
            [(badge_x, badge_y), (badge_x + badge_width, badge_y + badge_height)],
            radius=15,
            fill=self.ACCENT_COLOR,
            outline=self.TEXT_COLOR,
            width=4
        )
        
        # Draw badge text
        bbox = draw.textbbox((0, 0), badge_text, font=self.subtitle_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = badge_x + (badge_width - text_width) // 2
        text_y = badge_y + (badge_height - text_height) // 2 - 5
        
        draw.text((text_x, text_y), badge_text, font=self.subtitle_font, fill=self.TEXT_COLOR)
    
    def create_test_thumbnail(self):
        """Tạo thumbnail test"""
        test_title = "🔥 [TOEIC PART 3] Luyện Nghe Tiếng Anh Song Ngữ - Chủ đề Health 🔥"
        return self.create_thumbnail(test_title, "test_video.mp4", "test_thumbnail.jpg")


if __name__ == "__main__":
    # Test thumbnail generation
    generator = ThumbnailGenerator()
    thumbnail_path = generator.create_test_thumbnail()
    print(f"✅ Test thumbnail created: {thumbnail_path}")
