from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pynput import keyboard
import time
import os
import traceback

# Initialize data storage
collected_html_sections = []

# Set up browser (NOT headless so you can see and interact with it)
options = Options()
options.add_experimental_option("detach", True)  # Keeps browser open
driver = webdriver.Chrome(options=options)

# Navigate to login page
login_url = "http://localhost/laserfast/index.php"  # Replace with your actual login URL
driver.get(login_url)

# Prompt user to manually login
print("Please log in manually in the browser window...")
input("Press Enter when you've logged in successfully...")

print("Login successful! Now you can navigate the site.")
print("- Press 's' to save current page's legend-parts section")
print("- Press 'd' to debug page elements")
print("- Press 'q' to save all data and quit the script")

# Function to save current page section with debugging
def save_current_page():
    print("Starting to save current page's legend-parts section...")
    try:
        print(f"Current URL: {driver.current_url}")
        
        # Try to find the specific section
        print("Searching for <section id='legend-parts'>...")
        try:
            section = driver.find_element(By.CSS_SELECTOR, "section#legend-parts")
            print("Found the section!")
            
            # Get the outer HTML of the section
            html_content = section.get_attribute('outerHTML')
            print(f"Retrieved HTML content ({len(html_content)} characters)")
            
            # Add to our collection with URL and timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            collected_html_sections.append({
                "url": driver.current_url,
                "timestamp": timestamp,
                "html": html_content
            })
            
            # Save to file (both individual and combined files)
            # Create a unique filename based on timestamp
            sanitized_timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"section_{sanitized_timestamp}.html"
            
            # Save individual file
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # Save all sections to one file
            with open("all_sections.html", "w", encoding="utf-8") as f:
                for section_data in collected_html_sections:
                    f.write(f"\n<!-- URL: {section_data['url']} -->\n")
                    f.write(f"<!-- Timestamp: {section_data['timestamp']} -->\n")
                    f.write(section_data['html'])
                    f.write("\n\n" + "-"*80 + "\n\n")
            
            print(f"Saved section HTML to {filename}")
            print(f"Total sections collected: {len(collected_html_sections)}")
            
        except Exception as e:
            print(f"Error finding section: {e}")
            print("Section with id='legend-parts' not found on this page.")
            traceback.print_exc()
    except Exception as e:
        print(f"Unexpected error in save_current_page: {e}")
        traceback.print_exc()

# Debug function to check if the section exists or find alternatives
def debug_page():
    print("\n--- PAGE DEBUG INFO ---")
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
    
    # Try to find the section directly
    try:
        section = driver.find_element(By.CSS_SELECTOR, "section#legend-parts")
        print("Found <section id='legend-parts'>!")
        print(f"Section text preview: {section.text[:100]}...")
    except:
        print("Could NOT find <section id='legend-parts'>")
        
        # Look for any sections
        sections = driver.find_elements(By.TAG_NAME, "section")
        if sections:
            print(f"Found {len(sections)} other <section> elements:")
            for i, s in enumerate(sections[:5]):  # Show first 5 only
                try:
                    section_id = s.get_attribute('id') or "no-id"
                    section_class = s.get_attribute('class') or "no-class"
                    section_text = s.text[:50] + "..." if len(s.text) > 50 else s.text
                    print(f"  - Section {i+1}: id='{section_id}', class='{section_class}'")
                    print(f"    Text preview: '{section_text}'")
                except:
                    pass
        else:
            print("No <section> elements found on page")
            
            # Look for potential containers that might contain your data
            print("\nPotential alternative containers:")
            for selector in ["div", "article", "main", "div.content", "div.container"]:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Found {len(elements)} '{selector}' elements")
    
    print("\nSuggested next steps:")
    print("1. Use browser developer tools (F12) to verify the correct selector")
    print("2. Check if the section ID might be different")
    print("3. If needed, update the script with the correct selector")
    print("--- END DEBUG INFO ---\n")

# Set up keyboard shortcut listener
def on_press(key):
    try:
        # Press 's' to save current page data
        if key.char == 's':
            print("Saving current page section...")
            save_current_page()
        # Press 'd' to debug the page
        elif key.char == 'd':
            print("Debugging page elements...")
            debug_page()
        # Press 'q' to quit and save all data
        elif key.char == 'q':
            print("Saving and quitting...")
            # Save all sections to one file (final copy)
            with open("all_sections_final.html", "w", encoding="utf-8") as f:
                for section_data in collected_html_sections:
                    f.write(f"\n<!-- URL: {section_data['url']} -->\n")
                    f.write(f"<!-- Timestamp: {section_data['timestamp']} -->\n")
                    f.write(section_data['html'])
                    f.write("\n\n" + "-"*80 + "\n\n")
            print(f"Saved {len(collected_html_sections)} sections to all_sections_final.html")
            return False  # Stop listener
    except AttributeError:
        pass
    except Exception as e:
        print(f"Error in key handler: {e}")

# Start listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Keep script running
try:
    listener.join()
finally:
    driver.quit()