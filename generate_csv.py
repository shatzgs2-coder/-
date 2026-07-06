"""Generate Shopify product import CSV from products_master.json"""
import json
import csv
import html

with open('products_master.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Shopify CSV columns
csv_columns = [
    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags',
    'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name',
    'Option2 Value', 'Option3 Name', 'Option3 Value',
    'Variant SKU', 'Variant Grams', 'Variant Inventory Qty',
    'Variant Price', 'Variant Compare At Price', 'Variant Inventory Tracker',
    'Image Src', 'Variant Image', 'Status'
]

rows = []

for product in products:
    # Product metadata
    handle = product['handle']
    title = product['title_en']
    body_html = product['description_html']
    category = product['category']
    # Map Chinese categories to Google Product Category
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
    gpc = category_map.get(category, 'Home & Garden')
    
    tags = f"{category}, Wabi-Sabi, Minimalist, Handmade, Natural"
    vendor = product.get('supplier', 'Aela Daily')
    image = product.get('image_file', '')
    # Slugify image filename to avoid URL encoding issues
    image_slug = f"product-{product['id']:03d}.jpg"
    image_src = f"https://cdn.shopify.com/s/files/1/0000/0000/0000/files/{image_slug}"
    
    sizes = product.get('sizes', ['One Size'])
    colors = product.get('colors', ['Natural'])
    
    # For products with too many variants (>30), reduce to top variants
    if len(sizes) * len(colors) > 30:
        # Take first 3 sizes and first 3 colors
        sizes = sizes[:3]
        colors = colors[:3]
    
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
                row['Image Src'] = image_src
                row['Status'] = 'active'
                first_row = False
            
            # Option1 = Size, Option2 = Color
            if size_idx == 0 and color_idx == 0:
                row['Option1 Name'] = 'Size'
                row['Option1 Value'] = size
                if colors and colors[0] != 'Natural' or len(colors) > 1:
                    row['Option2 Name'] = 'Color'
                row['Option2 Value'] = color
            else:
                if size_idx > 0:
                    row['Option1 Value'] = size
                if colors and colors[0] != 'Natural' or len(colors) > 1:
                    if color_idx > 0:
                        row['Option2 Value'] = color
                elif color_idx > 0:
                    row['Option2 Value'] = color
            
            # SKU: AD-XXX-{size_code}-{color_code}
            size_code = size.replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '')[:20]
            color_code = color.replace(' ', '-').replace('/', '-')[:15]
            sku = f"{product['sku_prefix']}-{size_code}-{color_code}"
            row['Variant SKU'] = sku
            
            row['Variant Grams'] = '500'
            row['Variant Inventory Qty'] = '100'
            row['Variant Inventory Tracker'] = 'shopify'
            
            # Price
            row['Variant Price'] = str(product['price_eur'])
            row['Variant Compare At Price'] = str(product['compare_eur'])
            
            rows.append(row)

# Write CSV
csv_path = 'products_import.csv'
with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=csv_columns, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

# Count stats
total_rows = len(rows)
unique_handles = len(set(r.get('Handle', '') for r in rows))
print(f"Generated {total_rows} variant rows for {unique_handles} products")
print(f"Saved to {csv_path}")
