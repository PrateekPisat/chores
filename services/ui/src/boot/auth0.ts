import { boot } from 'quasar/wrappers';
import { createAuth0 } from '@auth0/auth0-vue';



export default boot(async ({ app }) => {
  app.use(
    createAuth0({
      domain: import.meta.env.VITE_AUTH0_DOMAIN,
      clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
      authorizationParams: {
        redirect_uri: window.location.origin
      }
    })
  );
});
