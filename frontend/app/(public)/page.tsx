/**
 * PublicPage shows the landing page with a link to channels.
 */
import Link from 'next/link';

export default function PublicPage() {
  return (
    <div>
      <h1>Welcome to the public page</h1>
      <Link href="/channels">Channels</Link>
    </div>
  );
}
