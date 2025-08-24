export default function RegisterPage() {
  // TODO: wire up form submission to call backend /api/v1/auth/register
  return (
    <form className="flex flex-col gap-2">
      <input type="email" placeholder="Email" required className="border p-2" />
      <input type="password" placeholder="Password" required className="border p-2" />
      <button type="submit" className="bg-green-500 text-white p-2">Register</button>
    </form>
  );
}
