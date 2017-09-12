# bokeh serve apps  -- 高校财务数据可视分析

### 文档说明：

1. 这是我在某单位实习时，为部门同事做的高校财务数据可视分析应用，由校际比较、时间序列、经费占比分析三个部分构成。由于实际使用的数据不能公开，我随机生成了一些数据，数据指标也仅以“数据1”等指代；但这并不影响对代码及可视效果的理解。三个可视子系统的实现代码 —— crossSection.py, timeSeries.py, ratioAnalysis.py —— 在code文件夹中。


2. 这次使用了Python的一个第三方库 —— [bokeh](https://bokeh.pydata.org/en/latest/) 。bokeh的灵活度高，尤其是如果你同时也会js的话，用bokeh可以做出相当漂亮的可视效果；基于bokeh的应用还支持数据流(实时更新)的可视化，当然也可以嵌入主流的web框架，比如 flask，django 等，可扩展性较强。我将这些应用嵌入了flask框架中用于展示，详情可见：https://vis-demo-bnufisher.c9users.io/

    我看到有人将bokeh比喻为Python可视化库中的d3, 但也承认bokeh目前仍无法撼动d3在可视化领域的霸主地位。好吧，其实如果熟悉js和d3的话，你可能也不会用bokeh了吧；而如果你和我一样，仅有Python基础，又需要做一个可视化的web应用，那么bokeh就是一个很好的选择了。


3. **实现项目需要的安装包见 requirements.txt文件。需要说明的是，目前numpy和bokeh包都有了更新的版本，且并不完全与当前的应用兼容。如果你fork后启用程序报错，请务必检查安装包的版本是否和我列出的一致。** 使用命令: pip install -r requirements.txt 即可自动安装这些包，当然，请在虚拟环境(virtualenv)下进行发开。


4. 除了bokeh包外，你还需要对pandas包较为熟悉，后者真乃神器，很多数据清洗和转换的需求用pandas都可以轻松实现。这两个包都有非常详细的官方文档，可参阅： pandas的  [tutorial](http://pandas.pydata.org/pandas-docs/stable/tutorials.html) 以及bokeh的  [reference](http://bokeh.pydata.org/en/latest/docs/reference.html) 。


#### 分享一下学习心得，如何尽快熟悉bokeh？

我把官方给出每个[server app example](http://bokeh.pydata.org/en/latest/docs/gallery.html#gallery) 的代码都手抄了一遍，再逐行把代码过了几遍，理解其中的逻辑。在学习这些例子的过程，我的bokeh server app应该怎么布局，需要哪些部件，就渐渐浮现了。

当然，学习官方样例只是一个起点。事实上，你想要的效果很可能在examples中找不到，这时可以查阅官方说明，有些效果还可能需要自己写js来实现。


#### Bonus

最后，推荐一下udemy上的这门课：[Interactive Data Visualization with Python & Bokeh](https://www.udemy.com/python-bokeh/) 。其中关于在 flask 框架中嵌入bokeh server app的介绍对我很有帮助。

 我购买的时候是10美元，价格比较实惠。老师在讨论区挺积极，几乎总是回答学习者的提问，而你的一些疑问可能已有人问过，不妨先搜一下吧。