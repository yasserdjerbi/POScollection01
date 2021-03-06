# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.translate import html_translate

class Partner(models.Model):
    _inherit = "res.partner"
    
    @api.onchange('student_id')
    def _onchange_student_id(self):
        if self.parent_id:
            self.isstudent = "true"

    issponsor = fields.Boolean(string='IsSponsor', default=False)
    istutor = fields.Boolean(string='IsTutor', default=False)
    isparent = fields.Boolean(string='IsParent', default=False)
    isstudent = fields.Boolean(string='IsStudent', default=False)
    testimonial = fields.Html('Description', translate=html_translate, sanitize_attributes=False)
    website_publish = fields.Boolean( default=False)
    res_parent_id = fields.Many2one('res.partner', string='Parent',
                                    domain=[('isparent', '=', True)])
    slide_parents = fields.Many2many('res.partner', 'res_partner_rel',
                                     'parent_id', 'partner_id',
                                     string='Parents',
                                     domain=[('isparent', '=', True)],
                                     help="Parent")
    slide_childrens = fields.Many2many('res.partner', 'res_partner_child_rel',
                                       'parent_id', 'partner_id',
                                       string='Children Devotee',
                                       help="Children")
    student_id = fields.One2many('res.partner', 'res_parent_id',
                                 string='Children')
    website_published_state = fields.Selection([('published','Published'),
                               ('unpublished','Un Published')],
                                string='Published state',default='unpublished')
    channel_student_partner_ids = fields.One2many('slide.channel.partner',
                                                  'partner_id',
                                                  domain=[('partner_id.isstudent', '=', True)],
                                                  string='Channel Partner')

    @api.multi
    def publish_button(self):
            
        if self.website_publish==True:
            return self.write({'website_publish': False})
        else:
            return self.write({'website_publish': True})
        
    @api.multi
    def base_website_publish_button(self):
        """ Publish the event for website user
            @param self:base
        """        
        if self.website_published:
            return self.write({'website_published': not self.website_published,
                               'website_published_state': 'unpublished'
                               })
        else:
            return self.write({'website_published': True,
                               'website_published_state': 'published'
                               })
