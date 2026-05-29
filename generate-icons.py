"""Generate PWA icons for 辣堡辅食日记"""
import math
import struct
import zlib

def create_png(width, height, color_hex):
    """Create a simple solid-color PNG file as bytes"""
    r, g, b = int(color_hex[1:3], 16), int(color_hex[3:5], 16), int(color_hex[5:7], 16)

    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    # IHDR
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)

    # IDAT: raw pixel data (row filter byte + RGB per pixel)
    raw = b''
    for y in range(height):
        raw += b'\x00'  # filter: none
        for x in range(width):
            raw += bytes([r, g, b])
    compressed = zlib.compress(raw)
    png += chunk(b'IDAT', compressed)

    # IEND
    png += chunk(b'IEND', b'')
    return png

def create_icon_png(size):
    """Create a rounded-square icon with heart emoji texture"""
    r, g, b = 227, 24, 55  # #E31837
    bg_r, bg_g, bg_b = 255, 245, 245  # #FFF5F5

    raw = b''
    center = size // 2
    radius = int(size * 0.42)  # inner circle radius

    for y in range(size):
        raw += b'\x00'  # filter: none
        for x in range(size):
            dx = x - center
            dy = y - center
            dist = math.sqrt(dx*dx + dy*dy)

            # Outer rounded square (background)
            corner = size * 0.12
            in_rect = True
            if x < corner and y < corner:
                in_rect = math.sqrt((x-corner)**2 + (y-corner)**2) < corner
            elif x > size - corner and y < corner:
                in_rect = math.sqrt((x-(size-corner))**2 + (y-corner)**2) < corner
            elif x < corner and y > size - corner:
                in_rect = math.sqrt((x-corner)**2 + (y-(size-corner))**2) < corner
            elif x > size - corner and y > size - corner:
                in_rect = math.sqrt((x-(size-corner))**2 + (y-(size-corner))**2) < corner

            if not in_rect:
                raw += bytes([bg_r, bg_g, bg_b])
                continue

            if dist < radius:
                # Inside circle: red background
                # Draw a simple heart shape using math
                hx = dx / radius
                hy = (dy + radius * 0.25) / radius  # shift down a bit

                # Heart equation: (x^2 + y^2 - 1)^3 - x^2*y^3 < 0
                heart_val = (hx*hx + hy*hy - 1)**3 - hx*hx * hy*hy*hy
                if heart_val < 0:
                    raw += bytes([255, 255, 255])  # white heart
                else:
                    raw += bytes([r, g, b])  # red fill
            elif dist < radius + size * 0.02:
                raw += bytes([r, g, b])  # ring
            else:
                raw += bytes([bg_r, bg_g, bg_b])

    # Build PNG
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xffffffff)
        return struct.pack('>I', len(data)) + c + crc

    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
    compressed = zlib.compress(raw)
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png

# Generate icons
for size in [192, 512]:
    data = create_icon_png(size)
    with open(f'icon-{size}.png', 'wb') as f:
        f.write(data)
    print(f'✅ Generated icon-{size}.png ({len(data)} bytes)')

print('Done!')
