from django.contrib import admin
from sign.models import Event,Guest

# Register your models here.

# 新建了 EventAdmin 类， 继承 django.contrib.admin.ModelAdmin 类， 保存着一个类的自定义配置，
# Admin 管理工具使用。 这里只自定义了一项： list_display， 它是一个字段名称的数组， 用于定义要在列表中显
# 示哪些字段。 当然， 这些字段名称必须是模型中的 Event()类定义的

# Admin 管理后台提供了的很强的定制性， 我们甚至可以非常方便生成搜索栏和过滤器。 重新
# 打开.../sign/admin.py 文件， 做如下修改。

class EventAdmin(admin.ModelAdmin):
    list_display = ['name','status','start_time','id']
    search_fields = ['name'] # 搜索栏
    list_filter = ['status'] # 过滤器

class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname','phone','email','sign','create_time','event']
    search_fields = ['realname','phone']  # 搜索栏
    list_filter = ['sign']  # 过滤器

# admin.site.register(Event)
# admin.site.register(Guest)

# 上面这些代码通知 admin 管理工具为这些模块逐一提供界面。


# 修改 admin.site.register()调用， 添加了 EventAdmin。 你可以这样理解： 用 EventAdmin 选项注册
# Event 模块。
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)

# 上面这些代码通知 admin 管理工具为这些模块逐一提供界面。
