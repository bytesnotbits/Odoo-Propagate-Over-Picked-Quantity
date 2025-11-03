Description of the "[stock.picking] Propagate Over-Picked Quantity" Automation Rule
1. Purpose: The Problem This Solves

This automated action exists to solve a core operational disconnect in the warehouse. Our warehouse staff frequently needs to adjust the quantity of an item during the picking process (e.g., picking a full 20,000 ft cable reel for a 5,000 ft order, or picking a full box of 8 serialized items for an order of 7).

By default, Odoo does not automatically carry this new, larger quantity forward. This forces users to manually re-enter the corrected quantity at every subsequent step (Pack, Pickup, Sign), leading to potential data entry errors and inefficiency. This automation bridges that gap, making the system's data reflect the physical reality of the warehouse workflow.

2. How and Why It Works: The Logic Explained

This script triggers automatically the moment any warehouse transfer (Pick, Pack, etc.) is validated. It then performs the following intelligent steps:

Finds the Original Order: The script first identifies the original Sales Order that initiated the transfer. It does this by looking at the transfer's direct link (sale_id) or its origin document name. This original order is used as a stable "source of truth" for the initial demand.

Compares Real vs. Requested: It compares the quantity that was actually processed in the current step against the quantity that was originally requested on the Sales Order.

Updates the Next Step's Demand: If the processed quantity is greater than the original demand, the script finds the next operation in the chain (e.g., the Pack step) and updates its Demand ("To Do") to match the new, larger quantity. This provides clear and accurate instructions for the user at the next stage.

Handles Different Product Types Intelligently:

For Bulk/Lot-Tracked Items (like cable reels): For maximum efficiency, the script also pre-fills the Done ("Quantity") field on the next step. This allows the user to simply click "Validate" without re-entering data.

For Serialized Items (like routers): The script smartly detects that the product is tracked by serial number and does not pre-fill the quantity. This prevents a bug where the quantity could be incorrectly multiplied and allows Odoo's standard, line-by-line serial number handling to work perfectly.

In essence, this automation ensures that a single, real-world quantity adjustment made by a user at the beginning of the process flows seamlessly and accurately through the entire four-stage workflow, saving time and dramatically improving data integrity.
