.class public Lid/periksaujian/mock/Chrome;
.super Landroid/webkit/WebChromeClient;

.field private final host:Lid/periksaujian/mock/MainActivity;

.method public constructor <init>(Lid/periksaujian/mock/MainActivity;)V
    .locals 0
    invoke-direct {p0}, Landroid/webkit/WebChromeClient;-><init>()V
    iput-object p1, p0, Lid/periksaujian/mock/Chrome;->host:Lid/periksaujian/mock/MainActivity;
    return-void
.end method

.method public onShowFileChooser(Landroid/webkit/WebView;Landroid/webkit/ValueCallback;Landroid/webkit/WebChromeClient$FileChooserParams;)Z
    .locals 2
    iget-object v0, p0, Lid/periksaujian/mock/Chrome;->host:Lid/periksaujian/mock/MainActivity;

    iget-object v1, v0, Lid/periksaujian/mock/MainActivity;->pending:Landroid/webkit/ValueCallback;
    if-eqz v1, :nocancel
    const/4 p1, 0x0
    invoke-interface {v1, p1}, Landroid/webkit/ValueCallback;->onReceiveValue(Ljava/lang/Object;)V

    :nocancel
    iput-object p2, v0, Lid/periksaujian/mock/MainActivity;->pending:Landroid/webkit/ValueCallback;

    invoke-virtual {p3}, Landroid/webkit/WebChromeClient$FileChooserParams;->createIntent()Landroid/content/Intent;
    move-result-object v1
    const/4 p1, 0x1
    invoke-virtual {v0, v1, p1}, Landroid/app/Activity;->startActivityForResult(Landroid/content/Intent;I)V
    return p1
.end method
