from odoo import fields, models, api
    
class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    proveedor_o_cliente = fields.Many2one('res.partner', string="Proveedor o Cliente", compute="_search_partner")
    nacionalidad = fields.Char(string="Nacionalidad")


    @api.depends('reference')
    def _search_partner(self):
        for rec in self:
            if rec.reference:
                registro = self.env['stock.picking'].search([('name', '=', rec.reference)])
                cliente = registro.partner_id
                rec.nacionalidad = cliente.nacionalidad
                rec.proveedor_o_cliente = cliente
            else:
                rec.proveedor_o_cliente = ''
                rec.nacionalidad = ''