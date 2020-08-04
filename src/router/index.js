import Vue from "vue";
import Router from "vue-router";
import Home from "../views/Home.vue";
import Profile from "../views/Profile.vue";
import Archives from "../views/Archives.vue";
import Categorylist from "../views/Categorylist.vue";
import ViewContents from "../views/ViewContents.vue";
import Howto from "../views/Howto.vue"
import Uploader from "../views/Uploader.vue"
import NotFound from "../views/NotFound.vue"
import { authGuard } from "../auth";

Vue.use(Router);

const isHowtoPageExists = function(to, from, next) {
  if(to.params.name === 'upload') {
    return next();
  }

  if(to.params.name === 'ofuse') {
    return next();
  }

  next({name: 'notFound'})
  return
}

const router = new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/profile",
      name: "profile",
      component: Profile,
      beforeEnter: authGuard
    },
    {
      path: "/archives",
      name: "archives",
      component: Archives,
      beforeEnter: authGuard
    },
    {
      path: "/categorylist/:slug",
      name: "categorylist",
      component: Categorylist,
      beforeEnter: authGuard
    },
    {
      path: "/view/:id",
      name: "viewcontents",
      component: ViewContents,
      beforeEnter: authGuard
    },
    {
      path: "/howto/:name",
      name: "howto",
      props: true,
      component: Howto,
      beforeEnter: isHowtoPageExists
    },
    {
      path: "/uploader",
      name: "uploader",
      props: true,
      component: Uploader,
      beforeEnter: authGuard
    },
    {
      name: 'notFound',
      path: '*',
      component: NotFound,
      meta: { title: 'お探しのページは見つかりませんでした' }
    }
  ]
});

export default router;
