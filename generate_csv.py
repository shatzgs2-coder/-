"""Generate Shopify-ready product import CSV — directly importable with images"""
import json
import csv
import os

with open('products_master.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Shopify CSV columns (official format)
csv_columns = [
    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags',
    'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name',
    'Option2 Value', 'Option3 Name', 'Option3 Value',
    'Variant SKU', 'Variant Grams', 'Variant Inventory Qty',
    'Variant Price', 'Variant Compare At Price', 'Variant Inventory Tracker',
    'Variant Requires Shipping', 'Variant Taxable',
    'Image Src', 'Variant Image', 'Image Position',
    'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
    'Status'
]

# Google Product Category mapping
category_map = {
    '桌布': 'Home & Garden > Linens & Bedding > Table Linen',
    '抱枕': 'Home & Garden > Home Decor > Throw Pillows',
    '挂毯': 'Home & Garden > Home Decor > Wall Hangings',
    '收纳篮': 'Home & Garden > Storage & Organization > Baskets',
    '收纳盒': 'Home & Garden > Storage & Organization > Baskets',
    '脏衣篮': 'Home & Garden > Storage & Organization > Laundry Baskets',
    '吊篮': 'Home & Garden > Home Decor > Hanging Planters',
    '花盆网兜': 'Home & Garden > Home Decor > Hanging Planters',
    '木浆棉抹布': 'Home & Garden > Household Supplies > Dish Cloths',
    '洗碗刷': 'Home & Garden > Household Supplies > Dish Brushes',
    '香薰蜡片': 'Home & Garden > Home Fragrance > Wax Melts',
    '香薰蜡烛': 'Home & Garden > Home Fragrance > Candles',
    '香薰扩香石': 'Home & Garden > Home Fragrance > Reed Diffusers',
    '香薰藤条': 'Home & Garden > Home Fragrance > Reed Diffusers',
    '鞋拔子': 'Home & Garden > Household Supplies > Shoe Care',
    '餐垫': 'Home & Garden > Kitchen & Dining > Placemats',
    '杯垫': 'Home & Garden > Kitchen & Dining > Coasters',
    '桌旗': 'Home & Garden > Linens & Bedding > Table Runners',
    '沙发盖布': 'Home & Garden > Linens & Bedding > Furniture Covers',
    'Beeswax Wrap': 'Home & Garden > Kitchen & Dining > Food Wraps',
}

rows = []
total_variants = 0

for product in products:
    handle = product['handle']
    title = product['title_en']
    body_html = product['description_html']
    category = product['category']
    gpc = category_map.get(category, 'Home & Garden')
    tags = f"{category}, Wabi-Sabi, Minimalist, Handmade, Natural, Aela Daily"
    vendor = product.get('supplier', 'Aela Daily')
    
    sizes = product.get('sizes', ['One Size'])
    colors = product.get('colors', ['Natural'])
    
    # Limit to max 30 variants per product for import sanity
    if len(sizes) * len(colors) > 30:
        sizes = sizes[:4]
        colors = colors[:4]
        if len(sizes) * len(colors) > 30:
            sizes = sizes[:3]
            colors = colors[:3]
    
    # Image filename
    image_file = f"product-{product['id']:03d}.jpg"
    seo_title = f"{title} | Aela Daily — Wabi-Sabi Home"
    seo_desc = f"Handcrafted {title.lower()} in {product.get('material', 'natural materials')}. Wabi-sabi aesthetic. Free EU shipping. 30-day returns."
    
    first_row = True
    for size_idx, size in enumerate(sizes):
        for color_idx, color in enumerate(colors):
            row = {}
            
            if first_row:
                row['Handle'] = handle
                row['Title'] = title
                row['Body (HTML)'] = body_html
                row['Vendor'] = vendor
                row['Type'] = gpc
                row['Tags'] = tags
                row['Published'] = 'TRUE'
                row['Image Src'] = image_file
                row['Image Position'] = '1'
                row['Image Alt Text'] = f'{title} — {category} by Aela Daily'
                row['SEO Title'] = seo_title
                row['SEO Description'] = seo_desc
                row['Gift Card'] = 'FALSE'
                row['Status'] = 'active'
                first_row = False
            
            # Option1 = Size, Option2 = Color
            if size_idx == 0 and color_idx == 0:
                row['Option1 Name'] = 'Size'
                row['Option1 Value'] = size
                if len(colors) > 1 or (len(colors) == 1 and colors[0] != 'Natural'):
                    row['Option2 Name'] = 'Color'
                row['Option2 Value'] = color
            else:
                if size_idx > 0:
                    row['Option1 Value'] = size
                if len(colors) > 1 or (len(colors) == 1 and colors[0] != 'Natural'):
                    if color_idx > 0:
                        row['Option2 Value'] = color
                elif color_idx > 0:
                    row['Option2 Value'] = color
            
            # SKU
            size_code = size.replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace('~', '-')[:20]
            color_code = color.replace(' ', '-').replace('/', '-').replace('&', 'and')[:15]
            sku = f"{product['sku_prefix']}-{size_code}-{color_code}"
            row['Variant SKU'] = sku
            
            row['Variant Grams'] = '500'
            row['Variant Inventory Qty'] = '100'
            row['Variant Inventory Tracker'] = 'shopify'
            row['Variant Requires Shipping'] = 'TRUE'
            row['Variant Taxable'] = 'TRUE'
            row['Variant Price'] = str(product['price_eur'])
            row['Variant Compare At Price'] = str(product['compare_eur'])
            
            rows.append(row)
            total_variants += 1

# Write CSV
csv_path = 'products_import.csv'
with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

unique_handles = len(set(r.get('Handle', '') for r in rows))
print(f"✅ Generated {total_variants} variant rows for {unique_handles} products")
print(f"✅ Saved to {csv_path}")
print(f"")
print(f"📦 File size: {os.path.getsize(csv_path) / 1024:.1f} KB")
