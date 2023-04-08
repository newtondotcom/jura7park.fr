from points.models import points
from django.contrib.auth.models import User


def joueur1():
    rep = points.objects.all().order_by('-point')[:1]
    joueur1 = """
    <li class="c-list__item">
          <div class="c-list__grid">
              <div class="c-flag c-place u-bg--transparent u-text--dark u-bg--yellow">1</div>
              <div class="c-media">
                  <img class="c-avatar c-media__img" src="{}">
                  <div class="c-media__content">
                      <div class="c-media__title">{}</div>
                      <a class="c-media__link u-text--small" href="{}" target="_blank">@{}</a>
                  </div>
              </div>
              <div class="u-text--right c-kudos u-text--yellow">
                  <div class="u-mt--8">
                      <strong>{}</strong> 👏
                  </div>
              </div>
          </div>""".format(rep[0].avatar,rep[0].surnom.username,'test','test',rep[0].point)
    return joueur1

def joueur3():
    rep = points.objects.all().order_by('-point')[:3]
    joueur3 = """
    <li class="c-list__item">
          <div class="c-list__grid">
              <div class="c-flag c-place u-bg--transparent u-text--dark u-bg--orange">3</div>
              <div class="c-media">
                  <img class="c-avatar c-media__img" src="{}">
                  <div class="c-media__content">
                      <div class="c-media__title">{}</div>
                      <a class="c-media__link u-text--small" href="{}" target="_blank">@{}</a>
                  </div>
              </div>
              <div class="u-text--right c-kudos u-text--yellow">
                  <div class="u-mt--8">
                      <strong>{}</strong> 👏
                  </div>
              </div>
          </div>""".format(rep[2].avatar,rep[2].surnom.username,'test','test',rep[2].point)
    return joueur3

def joueur2():
    rep = points.objects.all().order_by('-point')[:2]
    joueur2 = """
    <li class="c-list__item">
          <div class="c-list__grid">
              <div class="c-flag c-place u-bg--transparent u-text--dark u-bg--teal">2</div>
              <div class="c-media">
                  <img class="c-avatar c-media__img" src="{}">
                  <div class="c-media__content">
                      <div class="c-media__title">{}</div>
                      <a class="c-media__link u-text--small" href="{}" target="_blank">@{}</a>
                  </div>
              </div>
              <div class="u-text--right c-kudos u-text--yellow">
                  <div class="u-mt--8">
                      <strong>{}</strong> 👏
                  </div>
              </div>
          </div>""".format(rep[1].avatar,rep[1].surnom.username,'test','test',rep[1].point)
    return joueur2



def text():
    string = ""
    rep = points.objects.all().order_by('-point')[:20]
    print(len(rep))
    for j in range(2,len(rep)-1):
        print(j)
        joueur = """
        <li class="c-list__item">
            <div class="c-list__grid">
                <div class="c-flag c-place u-bg--transparent">{}</div>
                <div class="c-media">
                    <img class="c-avatar c-media__img" src="{}">
                    <div class="c-media__content">
                        <div class="c-media__title">{}</div>
                        <a class="c-media__link u-text--small" href="{}" target="_blank">@{}</a>
                    </div>
                </div>
                <div class="u-text--right c-kudos">
                    <div class="u-mt--8">
                        <strong>{}</strong> 👍
                    </div>
                </div>
            </div>
        </li>
        """.format(rep[j].avatar,rep[j].surnom.username,'test','test',rep[j].point)
        string += joueur
    return string
    