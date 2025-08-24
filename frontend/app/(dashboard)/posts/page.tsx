import { PdfViewer } from '../../../lib/pdf';
import VideoPlayer from '../../../components/VideoPlayer';
import GifPlayer from '../../../components/GifPlayer';
import LinkPreview from '../../../components/LinkPreview';

export default function PostsPage() {
  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold">Embed Media</h1>
      <PdfViewer
        src="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        pages={1}
      />
      <VideoPlayer src="https://www.w3schools.com/html/mov_bbb.mp4" />
      <GifPlayer src="https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif" alt="Cat" />
      <LinkPreview url="https://example.com" />
    </div>
  );
}
