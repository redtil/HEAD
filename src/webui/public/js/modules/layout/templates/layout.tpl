<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
    <div id="navbar-container" class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                    data-target="#bs-example-navbar-collapse-1">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>

            <a class="navbar-brand" href="#">
                <img id="logo" class="pull-left" src="/public/img/H.png" alt=""/>
                <span id="app-title"></span>
            </a>

            <span id="notifications" class="pull-left">
                <span id="app-connecting" class="label label-warning">Connecting... Please wait</span>
                <span id="app-connection-error" class="label label-danger" style="display: none">Connection error. Click to refresh</span>
            </span>
        </div>
        <div id="app-navbar" class="collapse navbar-collapse">
            <ul class="nav navbar-nav navbar-right">
                <li><button title="Report a bug" class="app-report-button btn btn-default pull-right"><i
                        class="fa fa-exclamation-circle"></i></button>
                </li>
            </ul>
            <ul id="app-nav" class="nav navbar-nav navbar-right">
                <li><a href="#/puppeteering">Puppeteering</a></li>
                <li><a href="#/performances">Performances</a></li>
                <li><a href="#/gestures">Gestures</a></li>
                <li><a href="#/expressions">Expressions</a></li>
                <li><a href="#/motors">Motors</a></li>
                <li><a href="#/interactions">Chat</a></li>
            </ul>
            <ul id="app-admin-nav" class="nav navbar-nav navbar-right">
                <li><a href="#/admin/monitor">Monitoring</a></li>
                <li><a href="#/admin/animations">Animations</a></li>
                <li><a href="#/admin/expressions">Expressions</a></li>
                <li><a href="#/admin/motors">Motors</a></li>
                <li><a href="#/admin/settings">Settings</a></li>
            </ul>
        </div>
    </div>
</nav>

<div id="app-content"></div>
