from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import requests

def fetcher(url):
    """Fetch KT Telecom page content and translate from Korean to English"""

    # Fetch the webpage
    response = requests.get(url)
    response.raise_for_status()
    
    # Parse HTML
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Find the specific div
    target_div = soup.find('div', id='swiper-backup')

    return target_div

def parse_plan(soup):
    """Extract the plan names and benefits, and translate them to English"""

    plan_slides = soup.find_all('div', {"data-target": "yogo"})

    all_plans = {}

    for slide in plan_slides:
        # Extract the plan name and details
        title = slide.find('div', class_='title').text.strip()
        title = GoogleTranslator(source='ko', target='en').translate(title)

        # Initialize plan details
        plan_details = {
            'features': [],
            'benefits': [],
            'price': ''
        }

        # Extract features from rows
        rows = slide.find_all('div', class_='row')
        for row in rows:
            cols = row.find_all('div', recursive=False)
            if len(cols) == 2:
                feature = {
                    'name': GoogleTranslator(source='ko', target='en').translate(cols[0].text.strip()),
                    'value': GoogleTranslator(source='ko', target='en').translate(cols[1].text.strip())
                }
                plan_details['features'].append(feature)
        
        # Extract benefits from li elements
        benefits = slide.find_all('li')
        for benefit in benefits:
            benefit_text = ''
            # Get the main text
            benefit_text = GoogleTranslator(source='ko', target='en').translate(benefit.get_text(strip=True))
            plan_details['benefits'].append(benefit_text)
        
        # Extract price (remove non-numeric characters)
        total_div = slide.find('div', class_='total')
        if total_div and total_div.find('strong'):
            price = total_div.find('strong').text.strip()
            plan_details['price'] = price
        
        # Add plan to dictionary
        all_plans[title] = plan_details

    #     data = row.find('p', class_='plan-data').text.strip()
    return all_plans
        

    # translated_content = GoogleTranslator(source='auto', target='en').translate(target_div.text)

def print_plans(plans):
    """Print plans in a readable format"""
    print("\nKT Telecom Cell Phone Plans\n")
    
    for i, (plan_name, details) in enumerate(plans.items(), 1):
        print(f"{i}. {plan_name}")
        print(f"    Price: ₩{details['price']}")
        
        print("    Features:")
        for feature in details['features']:
            print(f"     • {feature['name']}: {feature['value']}")
        
        print("    Benefits:")
        for benefit in details['benefits']:
            print(f"     • {benefit}")
        
        print("\n")

def main():
    url = "https://shop.kt.com/direct/directUsim.do"
    soup = fetcher(url)
    if soup:
        plan_list = parse_plan(soup)
        print_plans(plan_list) 
    else:
        print("No plans found")

if __name__ == "__main__":
    main()