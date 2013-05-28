import reversion


class RadioAdmin(reversion.VersionAdmin):
    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"

    def save_model(self, request, obj, form, change):
        """
        Overridden `save_model` to allow any ModelAdmin that inherits this to
        specify a `auto_user_field` that automatically gets set to the current
        user logged in.
        """
        field_name = getattr(self, 'auto_user_field', None)
        if field_name:
            setattr(obj, field_name, request.user)
        super(RadioAdmin, self).save_model(request, obj, form, change)
