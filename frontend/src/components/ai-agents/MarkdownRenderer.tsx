"use client";

import React, { useState, useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";
import { Check, Copy } from "lucide-react";

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

function CodeBlock({
  language,
  code,
}: {
  language?: string;
  code: string;
}) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="my-2.5 rounded-xl border border-white/10 bg-slate-950 overflow-hidden shadow-lg">
      <div className="flex items-center justify-between px-3 py-1.5 bg-slate-900/90 border-b border-white/5 text-[10px] text-slate-400 font-mono">
        <span className="uppercase font-semibold tracking-wider text-cyan-400">
          {language || "code"}
        </span>
        <button
          type="button"
          onClick={handleCopy}
          className="flex items-center gap-1 px-2 py-0.5 rounded hover:bg-white/10 text-slate-300 hover:text-white transition-colors cursor-pointer"
        >
          {copied ? (
            <>
              <Check className="w-3 h-3 text-emerald-400" />
              <span className="text-emerald-400 font-sans">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="w-3 h-3" />
              <span className="font-sans">Copy</span>
            </>
          )}
        </button>
      </div>
      <pre className="p-3 overflow-x-auto text-xs font-mono text-slate-200 leading-relaxed scrollbar-thin">
        <code>{code}</code>
      </pre>
    </div>
  );
}

export default function MarkdownRenderer({
  content,
  className = "",
}: MarkdownRendererProps) {
  // Normalize unicode bullets (•, ●, ◦, ⁃) to markdown list format "- "
  const normalizedContent = useMemo(() => {
    if (!content) return "";
    return content.replace(/^([ \t]*)[•●◦⁃][ \t]+/gm, "$1- ");
  }, [content]);

  if (!normalizedContent) return null;

  return (
    <div
      className={`markdown-body text-xs text-slate-200 leading-relaxed space-y-1 ${className}`}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkBreaks]}
        components={{
          h1: ({ children }) => (
            <h1 className="text-base font-extrabold text-white mt-3.5 mb-2 pb-1.5 border-b border-white/10 flex items-center gap-2">
              <span>{children}</span>
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-sm font-bold text-indigo-300 mt-3 mb-1.5 flex items-center gap-2 border-b border-indigo-500/20 pb-1">
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 shrink-0" />
              <span>{children}</span>
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-[13px] font-bold text-cyan-300 mt-2.5 mb-1.5 flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0" />
              <span>{children}</span>
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-xs font-semibold text-slate-100 mt-2 mb-1 flex items-center gap-1.5">
              <span className="w-1 h-1 rounded-full bg-indigo-400 shrink-0" />
              <span>{children}</span>
            </h4>
          ),
          h5: ({ children }) => (
            <h5 className="text-xs font-semibold text-slate-200 mt-2 mb-1">
              {children}
            </h5>
          ),
          h6: ({ children }) => (
            <h6 className="text-[11px] font-semibold text-slate-300 mt-2 mb-1 uppercase tracking-wider">
              {children}
            </h6>
          ),
          p: ({ children }) => (
            <p className="text-xs text-slate-200 leading-relaxed my-1.5 first:mt-0 last:mb-0">
              {children}
            </p>
          ),
          ul: ({ children }) => (
            <ul className="list-disc pl-4 space-y-1 my-1.5 text-xs text-slate-200 marker:text-indigo-400 [&_ul]:my-0.5 [&_ul]:pl-4 [&_ol]:my-0.5 [&_ol]:pl-4">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal pl-4 space-y-1 my-1.5 text-xs text-slate-200 marker:text-cyan-400 [&_ul]:my-0.5 [&_ul]:pl-4 [&_ol]:my-0.5 [&_ol]:pl-4">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="leading-relaxed pl-0.5 text-slate-200 [&>p]:inline [&>p]:my-0">
              {children}
            </li>
          ),
          strong: ({ children }) => (
            <strong className="font-semibold text-white">
              {children}
            </strong>
          ),
          em: ({ children }) => (
            <em className="italic text-slate-300">
              {children}
            </em>
          ),
          blockquote: ({ children }) => (
            <blockquote className="border-l-2 border-indigo-400/80 bg-indigo-500/10 pl-3 py-1.5 my-2 rounded-r-lg text-slate-300 italic text-xs">
              {children}
            </blockquote>
          ),
          code({ className, children, ...props }: any) {
            const match = /language-(\w+)/.exec(className || "");
            const codeString = String(children).replace(/\n$/, "");
            const isMultiline = codeString.includes("\n");

            if (match || isMultiline) {
              return (
                <CodeBlock
                  language={match ? match[1] : undefined}
                  code={codeString}
                />
              );
            }

            return (
              <code
                className="font-mono text-[11px] px-1.5 py-0.5 mx-0.5 rounded-md bg-slate-800/90 text-cyan-300 border border-slate-700/60 font-medium inline-block align-baseline"
                {...props}
              >
                {children}
              </code>
            );
          },
          pre: ({ children }: any) => {
            return <>{children}</>;
          },
          table: ({ children }) => (
            <div className="overflow-x-auto my-3 rounded-xl border border-white/10 bg-slate-950/70 shadow-inner scrollbar-thin">
              <table className="w-full text-left text-xs border-collapse">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-slate-800/80 border-b border-white/10 text-slate-200">
              {children}
            </thead>
          ),
          tbody: ({ children }) => (
            <tbody className="divide-y divide-white/5">
              {children}
            </tbody>
          ),
          tr: ({ children }) => (
            <tr className="hover:bg-white/[0.03] transition-colors">
              {children}
            </tr>
          ),
          th: ({ children }) => (
            <th className="py-2 px-3 font-semibold text-[11px] uppercase tracking-wider text-slate-200">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="py-2 px-3 text-slate-300 text-xs font-normal">
              {children}
            </td>
          ),
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-cyan-400 hover:text-cyan-300 underline underline-offset-2 transition-colors font-medium inline-flex items-center gap-0.5"
            >
              {children}
            </a>
          ),
          hr: () => <hr className="my-3 border-t border-white/10" />,
        }}
      >
        {normalizedContent}
      </ReactMarkdown>
    </div>
  );
}
