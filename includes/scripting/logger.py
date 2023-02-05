from includes.typecheck import typecheck

class Logger:
    out = None
    def target(t):
        from includes.scripting.scripting import Scripting
        typecheck(t, Scripting)
        Logger.out = t
    
    def reset():
        Logger.out = None

def log(*args, **kwargs):
    if Logger.out: # Log to an Scripting Object Output
        Logger.out.output += ' '.join([str(i) for i in args]) + '\n'
    else: # Log to the Console
        print(*args, **kwargs)