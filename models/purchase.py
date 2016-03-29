from openerp.osv import osv, fields

class PurchaseOrderLine(osv.osv):
    _inherit = 'purchase.order.line'
    _columns = {
	'vendor_sku': fields.char('Vendor Sku'),
    }

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
	res = super(PurchaseOrderLine, self).onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, \
		uom_id, partner_id, date_order, fiscal_position_id, date_planned, \
		name, price_unit, state, context)

	if not product_id or not partner_id:
	    return res

	product_obj = self.pool.get('product.product')
	product = product_obj.browse(cr, uid, product_id)
	product_tmpl_id = product.product_tmpl_id.id
	query = "SELECT product_code FROM product_supplierinfo WHERE name = %s AND product_tmpl_id = %s" % \
		(partner_id, product_tmpl_id)
	cr.execute(query)
	results = cr.fetchone()
	if results:
	    res['value'].update({'vendor_sku': results[0]})
	return res
