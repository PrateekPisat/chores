import { boot } from 'quasar/wrappers';
import VueCookies from 'vue-cookies'

export default boot(({ app }) => {

  // default options config: { expires: '1d', path: '/', domain: '', secure: '', sameSite: 'Lax' , partitioned: false}
  app.use(VueCookies, { expires: '7d' })
});
