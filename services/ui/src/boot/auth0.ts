import { boot } from 'quasar/wrappers';
import { createAuth0 } from '@auth0/auth0-vue';


const auth0 = createAuth0({
  domain: import.meta.env.VITE_AUTH0_DOMAIN,
  clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
  authorizationParams: {
    redirect_uri: window.location.origin,
    audience: import.meta.env.VITE_AUTH0_AUDIENCE
  }
})

export default boot(async ({ app }) => {

  app.config.globalProperties.$auth0 = auth0;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API

  app.use(
    auth0
  );
});


function logout() {
  auth0.logout({
    logoutParams: {
      returnTo: window.location.origin,
    },
  });
}


export { logout, auth0 };
