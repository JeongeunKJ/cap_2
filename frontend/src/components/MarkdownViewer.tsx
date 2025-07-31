import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./tableStyle.css"; // Assuming you have styles for tables in this file

const MarkdownViewer = ({ content }) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        table: ({node, ...props}) => (
          <table className="custom-table" {...props} />
        ),
        th: ({node, ...props}) => (
          <th className="center-text" {...props} />
        ),
        td: ({node, ...props}) => (
          <td className="center-text" {...props} />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );
};

export default MarkdownViewer;