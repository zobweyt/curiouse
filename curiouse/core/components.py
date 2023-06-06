from django_components import component


@component.register("navbar")
class Navbar(component.Component):
    template_name = "components/navbar.html"
    
    def get_context_data(self, header: str, back: bool = False):
        return {
            "header": header,
            "back": back,
        }
        

@component.register("navbar-item")
class NavbarItem(component.Component):
    template_name = "components/navbar-item.html"
    
    def get_context_data(self, icon, title, viewname, badge=None, mobile=False):
        return {
            "icon": icon,
            "title": title,
            "viewname": viewname,
            "badge": badge,
            "mobile": mobile,
        }
        