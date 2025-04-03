import re
from bs4 import BeautifulSoup, NavigableString
import traceback

def parse_fluid_data(data):
    """Parses the fluid data, extracting the fluid name and fluid type."""
    fluids = []
    for i, line in enumerate(data.strip().split('\n')):
        print(f"DEBUG: Parsing line {i + 1}: '{line.strip()}'")
        try:
            match = re.search(r'^\s*([A-Za-z0-9\s,\-]+)\s+(VHL|VHG|HL|HG|LL|LG|NHL)\s*$', line)
            if match:
                name = match.group(1).strip()
                fluid_type = match.group(2).strip()
                fluids.append({'name': name, 'type': fluid_type})
                print(f"   -> DEBUG: Found: Name='{name}', Type='{fluid_type}'")
            else:
                print(f"   -> DEBUG: Warning: Skipping line - Invalid format: '{line.strip()}'")
        except Exception as e:
            print(f"   -> ERROR: Exception while parsing line {i + 1}: {e}")
            traceback.print_exc()
    print(f"DEBUG: Parsed {len(fluids)} fluids.")
    return fluids

def generate_fluid_table_html(fluids):
    """Generates an HTML table to display the fluid data."""
    html = """
    <div class="tab-content active" data-tab="all">
        <h2>All Fluid Types</h2>
        <input type="text" id="fluidSearch" onkeyup="searchFluidTable()" placeholder="Search for fluid...">
        <table class="fluid-table">
            <thead>
                <tr>
                    <th>Fluid Name</th>
                    <th>Fluid Type</th>
                </tr>
            </thead>
            <tbody id="fluidTableBody">
    """
    for fluid in fluids:
        html += f"""
            <tr>
                <td class="fluid-name">{fluid['name']}</td>
                <td class="fluid-code">{fluid['type']}</td>
            </tr>
        """
    html += """
            </tbody>
        </table>
    </div>

    <script>
    function searchFluidTable() {
        let input, filter, table, tbody, tr, td, i, txtValue;
        input = document.getElementById("fluidSearch");
        filter = input.value.toUpperCase();
        table = document.querySelector(".fluid-table");
        tbody = document.getElementById("fluidTableBody");
        tr = tbody.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
    </script>
    """
    print("DEBUG: Generated HTML table.")
    return html

# --- Main Execution ---
try:
    with open("Clean_Fluid_Data.txt", "r", encoding="utf-8") as file:
        fluid_data_raw = file.read()
    print("DEBUG: Successfully opened Clean_Fluid_Data.txt")
except FileNotFoundError:
    print("ERROR: Clean_Fluid_Data.txt not found.")
    exit()
except Exception as e:
    print(f"ERROR: Exception reading Clean_Fluid_Data.txt: {e}")
    traceback.print_exc()
    exit()

fluids = parse_fluid_data(fluid_data_raw)
fluid_table_html = generate_fluid_table_html(fluids)

try:
    with open("fluid-types.html", "r", encoding="utf-8") as file:
        fluid_types_html = file.read()
    print("DEBUG: Successfully opened fluid-types.html")
except FileNotFoundError:
    print("ERROR: fluid-types.html not found.")
    exit()
except Exception as e:
    print(f"ERROR: Exception reading fluid-types.html: {e}")
    traceback.print_exc()
    exit()

soup = BeautifulSoup(fluid_types_html, 'html.parser')

# More robust way to find the target div
target_div = soup.find("div", {"class": "tab-content", "data-tab": "all"})
if not target_div:
    target_div = soup.find("div", class_="tab-content")
    if target_div:
        if target_div.has_attr("data-tab") and target_div["data-tab"] != "all":
            target_div = None  # Found a div, but it's not the right data-tab

if target_div:
    print("DEBUG: Found target div in fluid-types.html")
    try:
        target_div.clear()
        new_content = BeautifulSoup(fluid_table_html, 'html.parser')
        for element in new_content.contents:
          if element.name is not None or isinstance(element, NavigableString):
            target_div.append(element)
        with open("fluid-types.html", "w", encoding="utf-8") as file:
            file.write(str(soup))
        print("DEBUG: Successfully updated fluid-types.html")
    except Exception as e:
        print(f"ERROR: Exception modifying fluid-types.html: {e}")
        traceback.print_exc()
        exit()
else:
    print("ERROR: Could not find the target div in fluid-types.html")
    exit()

print("DEBUG: Script completed.")
