// functions/_middleware.js
export const onRequest = async ({ request, env, next }) => {
  const unauthorized = () =>
    new Response("Authentication required", {
      status: 401,
      headers: { "WWW-Authenticate": 'Basic realm="Restricted"' }
    });

  const auth = request.headers.get("authorization") || "";
  if (!auth.startsWith("Basic ")) return unauthorized();

  const [user, pass] = atob(auth.slice(6)).split(":");
  if (user !== env.BASIC_USER || pass !== env.BASIC_PASS) return unauthorized();

  return next(); // пропускаем запрос к статике
};
