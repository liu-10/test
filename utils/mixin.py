from django.contrib.auth.decorators import login_required


class LoginRequiredMinxin(object):
    @classmethod
    def as_view(cls,**kwargs):
        # 调用父类的方法
        view = super(LoginRequiredMinxin,cls).as_view(**kwargs)
        return login_required(view)