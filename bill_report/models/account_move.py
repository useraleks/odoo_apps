# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import num2words as n2w

class ResPartner(models.Model):
    _inherit = "account.move"

    amount_total_in_words = fields.Char(string='Total en letras', compute='_compute_amount_total_in_words', store=True)
    
    @api.depends('amount_total')
    def _compute_amount_total_in_words(self):
        for record in self:
            amount = record.amount_total
            quetzales = int(amount)
            centavos = int((amount - quetzales) * 100)

            amount_in_words = n2w.num2words(quetzales, lang='es').capitalize()
            amount_in_words += ' quetzales'

            if centavos > 0:
                amount_in_words += ' con ' + n2w.num2words(centavos, lang='es').capitalize() + ' centavos'
                
            if centavos == 0:
                amount_in_words += ' con cero centavos'

            record.amount_total_in_words = amount_in_words
