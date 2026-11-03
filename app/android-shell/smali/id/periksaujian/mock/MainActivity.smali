.class public Lid/periksaujian/mock/MainActivity;
.super Landroid/app/Activity;

.field public pending:Landroid/webkit/ValueCallback;
.field private web:Landroid/webkit/WebView;

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 4
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

    new-instance v0, Landroid/webkit/WebView;
    invoke-direct {v0, p0}, Landroid/webkit/WebView;-><init>(Landroid/content/Context;)V
    iput-object v0, p0, Lid/periksaujian/mock/MainActivity;->web:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;
    move-result-object v1
    const/4 v2, 0x1
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V
    invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V

    new-instance v3, Landroid/webkit/WebViewClient;
    invoke-direct {v3}, Landroid/webkit/WebViewClient;-><init>()V
    invoke-virtual {v0, v3}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    new-instance v3, Lid/periksaujian/mock/Chrome;
    invoke-direct {v3, p0}, Lid/periksaujian/mock/Chrome;-><init>(Lid/periksaujian/mock/MainActivity;)V
    invoke-virtual {v0, v3}, Landroid/webkit/WebView;->setWebChromeClient(Landroid/webkit/WebChromeClient;)V

    new-instance v3, Lid/periksaujian/mock/Bridge;
    invoke-direct {v3, p0}, Lid/periksaujian/mock/Bridge;-><init>(Landroid/app/Activity;)V
    const-string v1, "AndroidBridge"
    invoke-virtual {v0, v3, v1}, Landroid/webkit/WebView;->addJavascriptInterface(Ljava/lang/Object;Ljava/lang/String;)V

    invoke-virtual {p0, v0}, Landroid/app/Activity;->setContentView(Landroid/view/View;)V

    const-string v1, "file:///android_asset/index.html"
    invoke-virtual {v0, v1}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V
    return-void
.end method

.method protected onActivityResult(IILandroid/content/Intent;)V
    .locals 2
    invoke-super {p0, p1, p2, p3}, Landroid/app/Activity;->onActivityResult(IILandroid/content/Intent;)V

    iget-object v0, p0, Lid/periksaujian/mock/MainActivity;->pending:Landroid/webkit/ValueCallback;
    if-eqz v0, :done

    invoke-static {p2, p3}, Landroid/webkit/WebChromeClient$FileChooserParams;->parseResult(ILandroid/content/Intent;)[Landroid/net/Uri;
    move-result-object v1
    invoke-interface {v0, v1}, Landroid/webkit/ValueCallback;->onReceiveValue(Ljava/lang/Object;)V

    const/4 v1, 0x0
    iput-object v1, p0, Lid/periksaujian/mock/MainActivity;->pending:Landroid/webkit/ValueCallback;

    :done
    return-void
.end method

.method public onBackPressed()V
    .locals 1
    iget-object v0, p0, Lid/periksaujian/mock/MainActivity;->web:Landroid/webkit/WebView;
    invoke-virtual {v0}, Landroid/webkit/WebView;->canGoBack()Z
    move-result v0
    if-eqz v0, :quit

    iget-object v0, p0, Lid/periksaujian/mock/MainActivity;->web:Landroid/webkit/WebView;
    invoke-virtual {v0}, Landroid/webkit/WebView;->goBack()V
    return-void

    :quit
    invoke-super {p0}, Landroid/app/Activity;->onBackPressed()V
    return-void
.end method
