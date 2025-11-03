# [Version 7 - Serial Number Bug Fix]
# This version adds a crucial check to handle serialized products correctly,
# preventing the quantity multiplication bug.

sale_order = record.sale_id
if not sale_order:
  if record.origin and (record.origin.startswith('S') or record.origin.startswith('s')):
    sale_order = env['sale.order'].search([('name', '=', record.origin)], limit=1)

if sale_order:
  for move in record.move_ids_without_package:
    sale_line = sale_order.order_line.filtered(lambda l: l.product_id == move.product_id)
    
    if not sale_line:
      continue
    
    sale_line = sale_line[0]

    original_demand_qty = sale_line.product_uom_qty
    total_processed_quantity = sum(move.move_line_ids.mapped('quantity'))

    if total_processed_quantity > (original_demand_qty + 0.001):
      for dest_move in move.move_dest_ids:
        # Step 1: Update the demand. This is always correct for all product types.
        dest_move.write({
          'product_uom_qty': total_processed_quantity
        })
        
        # Step 2: Tell Odoo to prepare/reserve the lines for the next step.
        dest_move._action_assign()
        
        # Step 3 (THE FIX): Check if the product is tracked by serial number.
        # We ONLY pre-fill the quantity for non-serial items (bulk, lot-tracked).
        if dest_move.product_id.tracking != 'serial':
          for line in dest_move.move_line_ids:
            line.write({
              'quantity': total_processed_quantity
            })
