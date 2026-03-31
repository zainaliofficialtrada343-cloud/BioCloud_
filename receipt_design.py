def format_items(items_list):
    rows = ""
    for item in items_list:
        rows += f"""
        <tr>
            <td>{item['name']}</td>
            <td class="text-center">{item['qty']}</td>
            <td class="text-right">{item['price']:.1f}</td>
        </tr>
        """
    return rows

# Jab aap template render karein, to aise likhein:
# html_content = template.render(
#     token_no="9",
#     patient_name="sameer",
#     items_rows=format_items(list_of_items) # Ye function rows generate karega
# )