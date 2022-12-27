from includes.typecheck import typecheck

class Logger:
    def target(t):
        from includes.scripting.scripting import Scripting
        typecheck(t, Scripting)
        Logger.target = t

def log(*args, **kwargs):
    # print(*args, **kwargs)
    Logger.target.output += ' '.join([str(i) for i in args])