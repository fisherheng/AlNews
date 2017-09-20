handlers = []
sub_handlers = []
ui_modules = {}

from alnews.handlers import wechat

sub_handlers.extend(wechat.sub_handlers)

# Append default 404 handler, and make sure it is the last one.

# wildcat subdomain handler for project should be the last one.


#for sh in sub_handlers:
#    sh.append((r".*", ErrorHandler))
