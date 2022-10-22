from .window import *
import gi # type: ignore

app = MyApp(application_id="one.k8ie.mphandy")
app.run(sys.argv)
