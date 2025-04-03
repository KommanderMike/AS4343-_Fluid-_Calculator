import re
import traceback  # Import the traceback module

def parse_fluid_data(data):
    """Parses the fluid data, extracting the fluid name and fluid type."""
    fluids = []
    for line in data.strip().split('\n'):
        print(f"Parsing line: '{line}'")  # Log the line being processed
        match = re.search(r'^\s*([A-Za-z0-9\s,\-]+)\s+(VHL|VHG|HL|HG|LL|LG|NHL)\s*$', line)
        if match:
            name = match.group(1).strip()
            fluid_type = match.group(2).strip()
            fluids.append({'name': name, 'type': fluid_type})
            print(f"  -> Found: Name='{name}', Type='{fluid_type}'")  # Log successful parse
        else:
            print(f"  -> Warning: Skipping line - Invalid format: '{line}'")  # Log skip
    print(f"Parsed {len(fluids)} fluids.")  # Log total parsed
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
    print("Generated HTML table.")  # Log HTML generation
    return html

try:
    with open("Clean_Fluid_Data.txt", "r", encoding="utf-8") as file:
        fluid_data_raw = file.read()
        print("Successfully opened Clean_Fluid_Data.txt")  # Log file open
    except FileNotFoundError:
        print("Error: Clean_Fluid_Data.txt not found.")
        exit()
    except Exception as e:  # Catch any other exceptions during file read
        print(f"Error reading Clean_Fluid_Data.txt: {e}")
        traceback.print_exc()  # Print the full traceback
        exit()

fluids = parse_fluid_data(fluid_data_raw)
fluid_table_html = generate_fluid_table_html(fluids)

try:
    with open("fluid-types.html", "r", encoding="utf-8") as file:
        fluid_types_html = file.read()
        print("Successfully opened fluid-types.html")  # Log file open
    except FileNotFoundError:
        print("Error: fluid-types.html not found.")
        exit()
    except Exception as e:  # Catch any other exceptions during file read
        print(f"Error reading fluid-types.html: {e}")
        traceback.print_exc()  # Print the full traceback
        exit()

start_index = fluid_types_html.find('<div class="tab-content active" data-tab="all">')
end_index = fluid_types_html.find('</div>', start_index, start_index + 500)

if start_index != -1 and end_index != -1:
    new_fluid_types_html = fluid_types_html[:start_index] + fluid_table_html + fluid_types_html[end_index]
    print("Successfully modified HTML content.")  # Log HTML modification
else:
    print("Error: Could not find the correct insertion points in fluid-types.html")
    exit()

try:
    with open("fluid-types.html", "w", encoding="utf-8") as file:
        file.write(new_fluid_types_html)
        print("Successfully wrote to fluid-types.html")  # Log file write
    except Exception as e:  # Catch any exceptions during file write
        print(f"Error writing to fluid-types.html: {e}")
        traceback.print_exc()  # Print the full traceback
        exit()

print("Script completed successfully.")