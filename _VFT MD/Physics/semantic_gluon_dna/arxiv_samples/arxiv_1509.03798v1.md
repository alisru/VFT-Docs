# Ordered Fields, the Purge of Infinitesimals from Mathematics and the Rigorousness of Infinitesimal Calculus

**arXiv ID**: 1509.03798v1

## Abstract
We present a characterization of the completeness of the field of real numbers in the form of a \emph{collection of several equivalent statements} borrowed from algebra, real analysis, general topology, and non-standard analysis. We also discuss the completeness of non-Archimedean fields and present several examples of such fields. As an application, we exploit the characterization of the reals to argue that the Leibniz-Euler infinitesimal calculus in the $17^\textrm{th}$-$18^\textrm{th}$ centuries was already a rigorous branch of mathematics -- at least much more rigorous than most contemporary mathematicians prefer to believe. By advocating our particular historical point of view, we hope to provoke a discussion on the importance of mathematical rigor in mathematics and science in general. This article is directed to all mathematicians and scientists who are interested in the foundations of mathematics and the history of infinitesimal calculus.

\documentclass[12pt,leqno]{amsart}
\usepackage{amssymb,amsmath,amsfonts,amsbsy, amsthm, xspace, latexsym, amscd, graphicx, fancyhdr,verbatim,enumitem}
\usepackage[colorlinks=true, pdfstartview=FitV, linkcolor=blue, citecolor=blue, urlcolor=blue]{hyperref}

\usepackage{latexsym}
\usepackage{amsmath,amsthm,amssymb,amsfonts}
\thispagestyle{empty}  
\allowdisplaybreaks
\setlength{\textwidth}{16cm} \setlength{\oddsidemargin}{0.2cm}
\setlength{\evensidemargin}{0.2cm} \setlength{\topmargin}{0.1cm}
\setlength{\footskip}{0.5cm}
\linespread{1}


\usepackage[normalem]{ulem}
\usepackage{color}
\newcommand{\remove}[1]{\textcolor{red}{\sout{#1}}}
\newcommand{\add}[1]{\textcolor{blue}{#1}}
\newcommand{\replace}[2]{\remove{#1}\;\add{#2}}
\newcommand{\nte}[1]{\textbf{NOTE:} \textcolor{red}{#1}}


\theoremstyle{definition}
\newtheorem{axiom}{Axiom}
\newtheorem{myth}{Myth}
\newtheorem{fact}{Fact}
\swapnumbers
\newtheorem{definition}{Definition}[section]
\newtheorem{remark}[definition]{Remark}
\newtheorem{remarks}[definition]{Remarks}
\newtheorem{example}[definition]{Example}
\newtheorem{examples}[definition]{Examples}
\newtheorem{notation}[definition]{Notation}
\newtheorem{warning}[definition]{Warning}
\theoremstyle{plain}
\newtheorem{theorem}[definition]{Theorem}
\newtheorem{proposition}[definition]{Proposition}
\newtheorem{lemma}[definition]{Lemma}
\newtheorem{corollary}[definition]{Corollary}
\newtheorem{snotation}[definition]{Short Notation}
\newtheorem{summary}[definition]{Summary}


\newcommand{\bra}{\ensuremath{\big\langle}}
\newcommand{\ket}{\ensuremath{\big\rangle}}
\newcommand{\supp}{\ensuremath{{\rm{supp}}}}
\newcommand{\card}{\ensuremath{{\rm{card}}}}
\newcommand{\dom}{\ensuremath{{\rm{dom}}}}
\newcommand{\ran}{\ensuremath{{\rm{ran}}}}
\newcommand{\mon}{\ensuremath{{\rm{mon}}}}
\newcommand{\st}{\ensuremath{{{\rm{st}}}}}
\newcommand{\rst}{\ensuremath{\ensuremath{{^\rho\st}\,}}}
\newcommand{\rqst}{{\ensuremath{\widehat{^\rho\st}}}}
\newcommand{\cl}{\ensuremath{{\rm{cl}}}}
\newcommand{\Ns}{\ensuremath{{\rm{Ns}}}}
\newcommand{\tr}{\ensuremath{{\rm{tr}}}}
\newcommand{\eqdef}{\ensuremath{\overset{\text{def}}{=}}}
\newcommand{\embed}{\ensuremath{\hookrightarrow}}
\newcommand{\emb}{\ensuremath{\hookrightarrow}}
\newcommand{\rest}{\!\!\ensuremath{\upharpoonright}\!} 
\newcommand{\conv}{\ensuremath{\circledast}}
\newcommand{\eval}{\ensuremath{\left. \right|}}
\newcommand{\Diff}{\ensuremath{{\rm{Diff}}}}
\newcommand{\eqae}{\ensuremath{ \overset{\centerdot}{=}}}
\newcommand{\lae}{\ensuremath{\overset{\centerdot}{<}}}
\newcommand{\gae}{\ensuremath{\overset{\centerdot}{>}}}
\newcommand{\geqae}{\ensuremath{\overset{\centerdot}{\geq}}}
\newcommand{\leqae}{\ensuremath{\overset{\centerdot}{\leq}}}
\newcommand{\inae}{\ensuremath{ \overset{\centerdot}{\in}}}
\newcommand{\ub}{\mathcal{UB}}
\newcommand{\cof}{\textrm{cof}}

\newlist{T-enum}{enumerate}{2}
\newlist{L-enum}{enumerate}{2}
\newlist{C-enum}{enumerate}{2}
\newlist{P-enum}{enumerate}{2}  
\newlist{Pf-enum}{enumerate}{2} 
\newlist{D-enum}{enumerate}{2}
\newlist{Ex-enum}{enumerate}{2}
\newlist{Exs-enum}{enumerate}{2}
\newlist{E-enum}{enumerate}{2}
\newlist{R-enum}{enumerate}{2}
\setlist[T-enum,1]{label=(\roman*),format=\bfseries\emph,leftmargin=*,labelindent=.1\parindent}
\setlist[T-enum,2]{label=(\alph*),format=\bfseries\emph,leftmargin=*,labelindent=.1\parindent}
\setlist[L-enum,1]{label=(\roman*),format=\bfseries\emph,leftmargin=*,labelindent=.1\parindent}
\setlist[L-enum,2]{label=(\alph*),format=\bfseries\emph,leftmargin=*,labelindent=.1\parindent}
\setlist[C-enum,1]{label=(\roman*),format=\bfseries\emph,leftmargin=*,labelindent=.1\parindent}
\setlist[C-enum,2]{label=(\alph*),format=\bfseries\emph,leftmargin=*,labelindent=.1\parindent}
\setlist[P-enum,1]{label=(\roman*),format=\bfseries\emph,leftmargin=*,labelindent=.1\parindent}
\setlist[P-enum,2]{label=(\alph*),format=\bfseries\emph,leftmargin=*,labelindent=.1\parindent}
\setlist[Pf-enum,1]{label=(\roman*), leftmargin=*,labelindent=.1\parindent}
\setlist[Pf-enum,2]{label=(\alph*), leftmargin=*,labelindent=.1\parindent}
\setlist[D-enum,1]{label=\textbf{\arabic*.},leftmargin=*,labelindent=.2\parindent}
\setlist[D-enum,2]{label=\textbf{(\alph*)},leftmargin=*,labelindent=.1\parindent}
\setlist[Ex-enum,1]{label=\textbf{\arabic*.},leftmargin=*,labelindent=.15\parindent}
\setlist[Ex-enum,2]{label=\textbf{\alph*.},leftmargin=*,labelindent=.15\parindent}
\setlist[Exs-enum,1]{label=\textbf{\arabic*.},leftmargin=*,labelindent=.15\parindent}
\setlist[Exs-enum,2]{label=\textbf{\alph*.},leftmargin=*,labelindent=.15\parindent}
\setlist[E-enum,1]{label=\textbf{\arabic*.},leftmargin=*,labelindent=.15\parindent}
\setlist[E-enum,2]{label=\textbf{\alph*.},leftmargin=*,labelindent=.15\parindent}
\setlist[R-enum,1]{label=\textbf{\arabic*.},leftmargin=*,labelindent=.15\parindent}
\setlist[R-enum,2]{label=\textbf{\alph*.},leftmargin=*,labelindent=.15\parindent}


\begin{document}
\vspace{0.5cm}


\title{Ordered Fields, the Purge of Infinitesimals from Mathematics and the Rigorousness of Infinitesimal Calculus}

\author{James F. Hall*\, and\, Todor D. Todorov**} 
 \address{Mathematics Department\\                
                        California Polytechnic State University\\
                        San Luis Obispo, California 93407, USA.}									\email{james@slohall.com \& ttodorov@calpoly.edu}

\thanks{*James F. Hall received his Master Degree in Mathematics from California Polytechnic State University at San Luis Obispo, in 2013. He presently works for \emph{Amazon Corporation} as a Software Development Engineer.}
\thanks{** Todor D. Todorov is a Professor in Mathematics at Cal Poly. He received his Ph.D. degree from University of Sofia \& Bulgarian Academy of Sciences in 1982 on the \emph{Problem of Multiplication of Schwartz Distributions} under the advisement of Academician Christo Ya. Christov. He is presently a Professor in Mathematics at California Polytechnic State University, San Luis Obispo, CA-93407, USA. Todor Todorov is particularly grateful to Professor Christov for introducing him to the theory of generalized functions - through infinitesimals - in an era when infinitesimals had already been expelled from mathematics and almost forgotten}
\thanks{***For a glimpse of Academician Professor Christo Ya. Christov mathematics and physics heritage, we refer to Mathematics  Genealogy  Project  (http://www.genealogy.math.ndsu.nodak.edu/id.php?id=\newline 177888)}.
\keywords{Ordered field, complete field, infinitesimals, infinitesimal calculus, non-standard analysis, valuation field, power series, Hahn field, transfer principle}
\subjclass{Primary: 03H05; Secondary: 01A50, 03C20, 12J10, 12J15, 12J25, 26A06}
\date{April 2015}
\maketitle

Dedicated to the memory of Christo Ya. Christov on the 100-th anniversary of his birth.***

\begin{abstract} We present a characterization of the completeness of the field of real numbers in the form of a \emph{collection of several equivalent statements} borrowed from algebra, real analysis, general topology, and non-standard analysis. We also discuss the completeness of non-Archimedean fields and present several examples of such fields. As an application, we exploit the characterization of the reals to argue that the Leibniz-Euler infinitesimal calculus in the $17^\textrm{th}$-$18^\textrm{th}$ centuries was already a rigorous branch of mathematics -- at least much more rigorous than most contemporary mathematicians prefer to believe. By advocating our particular historical point of view, we hope to provoke a discussion on the importance of mathematical rigor in mathematics and science in general. This article is directed to all mathematicians and scientists who are interested in the foundations of mathematics and the history of infinitesimal calculus.
\end{abstract}

\section{Introduction} 

	This article grew from a senior project of the first author (Hall~\cite{jHall11}), and a tutorial, written by the second author, used to introduce students in mathematics to non-standard analysis. The final version of this article, presented here, is directed towards professional mathematicians of all areas and levels of mathematical achievement (Fields medalists are not excluded), who have interest in the foundations of mathematics and the history of infinitesimal calculus. Our goal is to lay down the necessary mathematical background on ordered fields, which is necessary to discuss both the history of infinitesimal calculus and its connection to non-standard analysis. For some readers this text will be a helpful addition to the recent excellent book on the history of infinitesimals by Amir Alexander~\cite{aAlexander2014}.

	Our experience in discussing topics involving \emph{infinitesimals} has thus far indicated that modern mathematicians, unless specializing in non-standard analysis or model theory of fields, often do not have experience with ordered fields other than the subfields of $\mathbb R$.  Even the familiar field of rational functions $\mathbb R(t)$, which appears in any textbook on algebra, is rarely supplied with an ordering and presented as a simple example of a field with infinitesimals. We are trying to avoid the situation, in which after long and passionate discussions on the role of non-standard analysis in modern mathematics and its connection with the history of infinitesimal calculus, we realize that some participants of the discussion do not have any  rigorous definition of \emph{infinitesimal} in hand and do not have any example in mind for an ordered \emph{non-Archimedean field}. Notice that the finite fields $\mathbb Z_p$ and the the field of $p$-adic numbers $\mathbb Q_p$ are relatively popular, but neither of them is orderable.


	In Section~\ref{S: Preliminaries: Ordered Rings and Fields}, we recall the basic definitions and results about totally ordered fields -- not necessarily Archimedean. The content of this section, although algebraic and elementary in nature, is very rarely part of a standard mathematical education. In Section~\ref{S: Completeness of an Ordered Field}, we present a long list of definitions of different forms of completeness of an ordered field.  These definitions are not new, but they are usually spread throughout the literature of various branches of mathematics and presented at different levels of accessibility. In Section~\ref{S: Completeness of an Archimedean Field}, we present a characterization of the completeness of an Archimedean field -- that is to say, a characterization of the completeness of the reals. This characterization is in the form of a collection of ten equivalent statements borrowed from algebra, real analysis, general topology and non-standard analysis (Theorem~\ref{T: Completeness of an Archimedean Field}). Some parts of this \emph{collection} are well-known and can be found in the literature. We believe however, that this is the first time that the whole collection has appeared together.  In Section~\ref{S: Completeness of a Non-Archimedean Field}, we establish some basic results about the completeness of non-Archimedean fields which cannot be found in a typical textbook on algebra or analysis. In Section~\ref{S: Infinitesimals in Algebra and Non-Standard Analysis}, we present numerous examples of non-Archimedean fields -- both from algebra and non-standard analysis. The main purpose of the first six sections of our article is to emphasize the essential difference in the completeness of Archimedean and non-Archimedean fields and to prepare the reader for the following discussion on the history of calculus.

   In Section~\ref{S: The Purge of Infinitesimals from Mathematics}, we offer a short survey of the history of infinitesimal calculus, written in a \emph{polemic-like style}; our goal is to provoke a discussion on the topic, and we expect\add{,} and invite, {differing points of view}. One of the characterizations of the completeness of an Archimedean field presented in Theorem~\ref{T: Completeness of an Archimedean Field} (due originally to Keisler~\cite{jKeislerF}) is formulated in terms of infinitesimals and thus has a strong analog in the infinitesimal calculus of the $17^\textrm{th}$-$18^\textrm{th}$. We exploit this fact to re-evaluate ``with fresh eyes'' the rigorousness of the  $17^\textrm{th}$-$18^\textrm{th}$ centuries' infinitesimal calculus. In Section~\ref{S: How Rigorous Was the Leibniz-Euler Calculus}, we present a new, and perhaps surprising, answer to the question ``How rigorous was the infinitesimal calculus in the $18^\textrm{th}$ century?,'' arguing that the \emph{Leibniz-Euler infinitesimal calculus} was, in fact, much more rigorous than most modern mathematicians prefer to believe. It seems quite surprising that it took more than 200 years to realize how $18^\textrm{th}$ century mathematicians preferred to phrase the \emph{completeness} of the reals. But better late (in this case, very late) than never. We hope that this historical point of view might stir dormant mathematical passions and result in fruitful discussions on the importance and appreciation of mathematical rigor. 



\section{Preliminaries: Ordered Rings and Fields}\label{S: Preliminaries: Ordered Rings and Fields}
In this section we recall the main definitions and properties of totally ordered rings and fields (or simply, \emph{ordered rings and fields} for short), which are not necessarily Archimedean. We shortly discuss the properties of  infinitesimal, finite and infinitely large elements of a totally ordered field. For more details, and for the missing proofs, we refer the reader to (Lang~\cite{lang}, Chapter XI),  (van der Waerden~\cite{VanDerWaerden}, Chapter 11), (Hungerford~\cite{tHungerford}), (Ribenboim~\cite{riben}) and Dales \& Woodin~\cite{DalWoodin}.



\begin{definition}[Ordered Rings]\label{D: Totally Ordered Rings} Let $\mathbb{K}$ be a ring.  Then:
   \begin{D-enum}
\item $\mathbb K$ is \emph{orderable} if there exists a non-empty proper subset $\mathbb K_+$ of $\mathbb K$ such that (a) $0\notin\mathbb K_+$. (b) $\mathbb K_+$ is closed under the addition and multiplication in $\mathbb K$. (c) For every $x\in\mathbb K$ either $x=0$, $x\in\mathbb K_+$, or $-x\in\mathbb K_+$. We define an \emph{order relation} $<$ on $\mathbb K$ by $x<y$ if $y-x\in\mathbb K_+$. We refer to $(\mathbb{K}, +, \cdot,  <)$, denoted for short by $\mathbb{K}$, as an \emph{ordered ring}.

\item Let $a, b\in\mathbb{K}$ and $a\leq b$. We let $(a, b)=:\{x\in\mathbb{K}: a< x< b\}$ and 
$[a, b]=:\{x\in\mathbb{K}: a\leq x\leq b\}$.  A totally ordered ring $\mathbb{K}$  will be always supplied with the order topology, with the open intervals as basic open sets.
   \item  If $x\in\mathbb{K}$, we define the \emph{absolute value} of $x$ by $|x|=:\max(-x,x)$. If $A\subset\mathbb K$, we define the \emph{set of upper bounds} of $A$ by $\ub(A)=:\{x\in\mathbb K : (\forall a\in A)(a\le x)\}$. We denote by $\sup_\mathbb{K}(A)$ or, simply by $\sup(A)$, the \emph{least upper bound} of $A$ (if it exists).

   \item The \emph{cofinality} ${\rm cof}(\mathbb K)$ of $\mathbb K$ is the cardinality of the smallest unbounded subset of $\mathbb K$.

   \item Let $(I, \succcurlyeq)$ be a directed set (Kelley~\cite{jKelley}, Chapter 2)). A net $f: I\to\mathbb K$ is called  \emph{fundamental or Cauchy} if for every $\varepsilon\in\mathbb K_+$ there exists $h\in I$ such that $|f(i)-f(j)|<\varepsilon$ for all $i, j\in I$ such that $i, j\succcurlyeq h$.

   \item A totally ordered ring $\mathbb{K}$ is called \emph{Archimedean} if for every $x\in\mathbb{K}$, there exists $n\in\mathbb{N}$ such that $|x|\leq n$. 
   \end{D-enum}
\end{definition}

Notice that the field of the complex numbers $\mathbb C$, the finite fields $\mathbb Z_p$ and the field $\mathbb Q_p$ of real $p$-adic numbers ($p$ is a prime number) are non-orderable. Actually, a ring $\mathbb K$ is orderable if and only if $\mathbb K$ is \emph{formally real} in the sense that for every $n\in\mathbb N$ the equation $\sum_{k=1}^n x_k^2=0$ in $\mathbb K^n$ admits only the trivial solution $x_1=\dots=x_n=0$.

	Recall that there is a canonical embedding of $\mathbb Q$ into any ordered field $\mathbb K$ given by the unique extension of the map with $1_\mathbb Q\mapsto 1_\mathbb K$ to an isomorphism. This embedding is essential for the following definitions.

\begin{definition}[Infinitesimals, etc.]\label{D: Infinitesimals, etc.}
   Let $\mathbb{K}$ be a totally ordered field. We define the sets of \emph{infinitesimal}, \emph{finite}, and \emph{infinitely large} elements (respectively) by
   \begin{align*}
   \mathcal{I}(\mathbb{K})&=:\{x\in\mathbb{K} : |x|< 1/n \text{ for all } n\in\mathbb N\},\\
      \mathcal{F}(\mathbb{K})&=:\{x \in\mathbb{K} : |x|\le n  \text{ for some } n\in\mathbb N\},\\
      \mathcal{L}(\mathbb{K})&=:\{x \in\mathbb{K} : n<|x|  \text{ for all } n\in\mathbb N\}.
   \end{align*}

   We sometimes write $x\approx0$ if $x\in\mathcal I(\mathbb K)$ and $x\approx y$ if $x-y\approx 0$, in which case we say that $x$ is \emph{infinitesimally close} to $y$. If $S\subseteq\mathbb K$, we define the \emph{monad} of $S$ in $\mathbb K$ by $ \mu(S)=\{s+ds : s\in S,\, ds\in\mathcal I(\mathbb K)\}.$
\end{definition}

Following directly from the definitions above, we have a characterization of Archimedean rings in terms of infinitesimal and infinitely large quantities.

\begin{theorem}[Archimedean Property]\label{T: Archimedean Property}
  Let $\mathbb{K}$ be a totally ordered ring. Then the following are equivalent: (i) $\mathbb{K}$ is Archimedean. (ii) $\mathcal{F}(\mathbb{K})=\mathbb{K}$. (iii) $\mathcal L(\mathbb K)=\varnothing$. If $\mathbb{K}$ is a field, then each of the above is also equivalent to $\mathcal I(\mathbb K)=\{0\}$.  
\end{theorem}

\begin{remark}  Notice that Archimedean rings (which are not fields) might have non-zero infinitesimals. Indeed,  if $\mathbb K$ is a non-Archimedean field, then $\mathcal F(\mathbb K)$ is always an Archimedean ring (which is not a field), but it has non-zero infinitesimals (see Example~\ref{Ex: Field of Rational Functions} below).

\end{remark}

To help illuminate the use of these definitions, we give an example of a non-Archimedean field achieved by a simple ordering of the well known field of rational functions over $\mathbb Q$. More examples of non-Archimedean fields will appear in Section~\ref{S: Infinitesimals in Algebra and Non-Standard Analysis}.

\begin{example}[Field of Rational Functions]\label{Ex: Field of Rational Functions} Let $\mathbb K$ be an Archimedean ordered field (e.g. $\mathbb K=\mathbb Q$ or $\mathbb K=\mathbb R$). Let $\mathbb K[t]$ denote the ring of polynomials in one variable with coefficients in $\mathbb K$. We endow $\mathbb K[t]$ an order relation by: $f>0$ in $\mathbb K[t]$ if $a_0>0$ in $\mathbb K$, where $a_0$ stands for the coefficient in front the lowest power of $t$ in $f\in\mathbb K[t]$.  Then the field of \emph{rational functions}, $\mathbb K(t)$, is defined either as the \emph{field of fractions} of the ring $\mathbb K[t]$ in the sense of algebra (with the order inherited from $\mathbb K[t]$) or, equivalently, as the \emph{factor set} $\mathbb K(t)=S_{\mathbb K}/\sim$, where $S_{\mathbb K}=:\left\{p(t)/q(t) : p, q\in\mathbb K[t]\emph{ and }q\not=0\right\}$ is the set of the rational functions and $\sim$ is an equivalence relation on $S_{\mathbb K}$ defined by $f\sim g$ if $f(t)=g(t)$ holds in $\mathbb K$ for all sufficiently small $t\in\mathbb Q_+$.  In the latter construction we supply $\mathbb K(t)$ with the following ordering: $f< g$ in $\mathbb{K}(t)$ if $f(t)<g(t)$ holds in $\mathbb K$ for all sufficiently small $t\in\mathbb Q_+$. The field $\mathbb{K}(t)$ is non-Archimedean: $t, t^2, t+t^2$, etc. are positive infinitesimals. Indeed, for every $n\in\mathbb N$ we have $0<t<1/n$ in $\mathbb K$ for all sufficiently small $t\in\mathbb Q_+$. Thus $0<t<1/n$ in 
$\mathbb K(t)$ which means that $t$ is a positive infinitesimal (and similarly for the rest). Also, $1+t, 2+t^2, 3+t+t^2$, etc. are finite, but non-infinitesimal, and $1/t, 1/t^2, 1/(t+t^2)$, etc. are infinitely large elements of  $\mathbb{K}(t)$. Notice that the algebraic definition of $\mathbb{K}(t)$ (as the field of fractions) makes sense even for non-Archimedean fields $\mathbb K$.
\end{example}

\begin{theorem}\label{T: Maximal Ideal}
  Let $\mathbb{K}$ be a totally ordered field. Then $\mathcal{F}(\mathbb{K})$ is an Archimedean ring and $\mathcal{I}(\mathbb{K})$ is a maximal ideal of $\mathcal{F}(\mathbb{K})$. Moreover, $\mathcal{I}(\mathbb{K})$ is a \emph{convex ideal} in the sense that $a\in\mathcal{F}(\mathbb{K})$ and $|a|\le b\in\mathcal{I}(\mathbb{K})$ implies $a\in\mathcal{I}(\mathbb{K})$. Consequently $\mathcal{F}(\mathbb{K})/\mathcal{I}(\mathbb{K})$ is a totally ordered Archimedean field.
\end{theorem}     

\begin{remark}[Indivisibles?] The infinitesimals in $\mathbb K$ are always \emph{divisible} in the sense that if $dx\in\mathbb K$ is a non-zero infinitesimal, so is $dx/n$ for every $n\in\mathbb N$. For the history and philosophy of \emph{indivisibles} in the early years of infinitesimal calculus we refer the reader to Alexander\cite{aAlexander2014}. 
\end{remark}

\begin{definition}[Valuation on an Ordered Field]\label{D: Valuation on an Ordered Field} Let $\mathbb K$ be a totally ordered field. Then:
\begin{D-enum}
\item The mapping $v:\mathbb K\to \mathbb R\cup\{\infty\}$ is called a \emph{non-Archimedean valuation} on $\mathbb K$ if, for every $x,y\in\mathbb K$ the properties:
\begin{D-enum}
    \item $v(x)=\infty$ if and only if $x=0$,
    \item $v(xy)=v(x)+v(y)$ (\emph{Logarithmic property}),
    \item $v(x + y)\ge\min\{v(x), v(y)\}$ (\emph{Ultrametric Inequality}),
    \item $|x| < |y|$ implies $v(x) \ge v(y)$ (\emph{Convexity property}),
  \end{D-enum}
hold.
  The structure $(\mathbb K,v)$, denoted as $\mathbb K$ for short, is called an \emph{ordered valuation field}.
 
	\item We define the \textbf{valuation norm} $||\cdot||_v: \mathbb K\to\mathbb R$ by the formula $||x||_v=e^{-v(x)}$ with the understanding that $e^{-\infty}=0$.  Also, the formula  $d_v(x, y)=||x-y||_v$ defines the \emph{valuation metric} $d_v: \mathbb K\times\mathbb K\to\mathbb R$. We denote by $(\mathbb{K}, d_v)$ the \emph{associated metric space}.
\item The valuation $v$ is called \textbf{trivial} if $v(x)=0$ for all non-zero $x\in\mathbb K$.

\end{D-enum}
\end{definition}

\begin{example}
   The field of rational functions above is a valuation field with the valuation $v:\mathbb{K}(t)\to \mathbb R\cup\{\infty\}$ defined as follows: If $P\in\mathbb{K}[t]$ is a non-zero polynomial, then $v(P)$ is the lowest power of $t$ in $P$ and if $Q$ is another non-zero polynomial, then $v(P/Q)=v(P)-v(Q)$.   
\end{example}

The name ``non-Archimedean valuation'' is justified by the following result (the proof is left to the reader):

\begin{theorem}[Valuation on an Archimedean Field]\label{C: Valuation on an Archimedean Field} Let
$(\mathbb{K}, v)$  be an ordered valuation field. If  $\mathbb{K}$ is
Archimedean, then the valuation $v$ is  trivial. Consequently, if $v$ is non-trivial, then $\mathbb K$ is a non-Archimedean field. 
\end{theorem}

\begin{remark}[$p$-Adic Valuation] Notice that the above theorem fails if the valuation $v$ is defined by (a)-(c) only (without property (d) in Definition~\ref{D: Valuation on an Ordered Field}). Indeed, let $p$ be a prime number. Every non-zero rational number $x$ can be
uniquely presented in the form $x=(a/b)p^\alpha$, where $a, b, \alpha\in\mathbb{Z}$ and $a$
and $b$ are not divisible by $p$. The $p$-\textbf{adic valuation} on
$\mathbb{Q}$ is defined by $v(0)=\infty$ and by
$v(x)=\alpha$ for $x\in\mathbb{Q},\, x\not=0$ (Fernando Q. Gouv\^{e}a~\cite{fqGouv}). Notice that $v_p$ is non-convex; for example, $v_2(2)=1<2=v_p(12)$. Notice as well that $v_p$ is non-trivial although $\mathbb Q$ is an Archimedean field (by Definition~\ref{D: Totally Ordered Rings} adopted in this article). 
\end{remark}




\section{Completeness of an Ordered Field}\label{S: Completeness of an Ordered Field}
  
We provide a collection of definitions of several different forms of completeness of a totally ordered field -- not necessarily Archimedean. The relations between these different forms of completeness will be discussed in the next two sections. 

\begin{definition}[Completeness of a Totally Ordered Field]\label{D: Completeness of a Totally Ordered Field}
  Let $\mathbb{K}$ be a totally ordered field.
  \begin{D-enum}
  \item If $\kappa$ is an uncountable cardinal, then $\mathbb{K}$ is called \emph{Cantor $\kappa$-complete} if every family $\{[a_\gamma,b_\gamma]\}_{\gamma\in \Gamma}$ of fewer than $\kappa$ closed bounded intervals in $\mathbb{K}$ with the finite intersection property (F.I.P.) has a non-empty intersection, $\bigcap_{\gamma\in \Gamma} [a_\gamma,b_\gamma]\neq \varnothing$. We say that $\mathbb{K}$ is \emph{sequentially Cantor complete} if every nested sequence of bounded closed intervals in $\mathbb{K}$ has a non-empty intersection (that is to say that $\mathbb K$ is Cantor $\aleph_1$-complete, where $\aleph_1$ is the successor of $\aleph_0=\card(\mathbb{N})$).  We say that $\mathbb{K}$ is simply \emph{Cantor complete} if every family $\{[a_\gamma,b_\gamma]\}_{\gamma\in \Gamma}$ with the finite intersection property  and with $\card(\Gamma)\leq\cof(\mathbb K)$, has a non-empty intersection (that is to say that $\mathbb K$ is Cantor $\kappa^+$-complete for $\kappa=\cof(\mathbb K)$, where $\kappa^+$ is the successor of $\kappa$).

   \item Let $\mathbb K$ be Archimedean and $^*\mathbb K$ be a non-standard extension (Davis~\cite{davis},  Lindstr\o m~\cite{lindstrom} and/or  Example~\ref{Ex: Non-Standard Real Numbers} in this article). Let $\mathcal F(^*\mathbb K)$ and $\mathcal I(^*\mathbb K)$ denote the sets of finite and infinitesimal elements in $^*\mathbb K$, respectively (see Definition~\ref{D: Infinitesimals, etc.}). Then we say that $\mathbb{K}$ is \emph{Leibniz complete} if every $x\in\mathcal{F}(^*\mathbb{K})$ can be presented (uniquely) in the form $x=r+dx$ for some $r\in\mathbb K$ and some $dx\in\mathcal{I}(^*\mathbb{K})$. 
   \item $\mathbb K$ is \emph{Heine-Borel complete} if a subset $A\subseteq \mathbb K$ is compact if and only if $A$ is closed and bounded.

   \item We say that $\mathbb{K}$ is \emph{monotone complete} if every bounded increasing sequence is convergent.
 
   \item We say that $\mathbb{K}$ is \emph{Weierstrass complete} if every bounded sequence has a convergent subsequence.

   \item We say that $\mathbb{K}$ is \emph{Bolzano complete} if every bounded infinite set has a cluster point.

   \item $\mathbb{K}$ is \emph{Cauchy complete} (or, simple \emph{complete} for short) if it can not be embedded into another field as a dense subfield. (This is equivalent to the property that every fundamental $I$-net in $\mathbb K$ is convergent, where $I$ is an index set with $\card(I)={\rm cof}(\mathbb K)$.) 
      
   \item We say that $\mathbb{K}$ is simply \emph{sequentially complete} if every fundamental (Cauchy) sequence in $\mathbb K$ converges (regardless of whether or not $\cof(\mathbb K)=\aleph_0$).

   \item $\mathbb{K}$ is \emph{Dedekind complete} (or \emph{order complete}) if every non-empty subset of $\mathbb{K}$ that is bounded from above has a supremum.
 
   \item Let $\mathbb{K}$ be Archimedean. Then $\mathbb{K}$ is \emph{Hilbert complete} if $\mathbb{K}$ is a maximal Archimedean field in the sense that $\mathbb K$ has no proper totally ordered Archimedean field extension.

   \item  If $\kappa$ is an infinite cardinal, $\mathbb K$ is called \emph{algebraically $\kappa$-saturated} if every family $\{(a_\gamma,b_\gamma)\}_{\gamma\in \Gamma}$ of fewer than $\kappa$ open intervals in $\mathbb K$ with the finite intersection property has a non-empty intersection, $\bigcap_{\gamma\in \Gamma} (a_\gamma,b_\gamma)\neq \emptyset$. If $\mathbb{K}$ is algebraically $\card(\mathbb K)$-saturated, then we simply say that $\mathbb{K}$ is \emph{algebraically saturated}.

\item A metric space is called\, \emph{spherically complete} if every
nested sequence of closed balls has
nonempty intersection. In particular, an ordered valuation field $(\mathbb K, v)$ is \emph{spherically complete} if the associated metric space $(\mathbb K, d_v)$ is spherically complete (Definition~\ref{D: Valuation on an Ordered Field}).
  \end{D-enum}
\end{definition}

\begin{remark}[Terminology]\label{R: Terminology} Here are some remarks about the above terminology:
  
\begin{itemize}
  \item \emph{Leibniz completeness} appears in the early Leibniz-Euler Infinitesimal Calculus as the statement that ``every finite number is infinitesimally close to a unique usual quantity.'' Here the ``usual quantities'' are what we now refer to as the real numbers and $\mathbb{K}$ in the definition above should be identified with the set of the reals $\mathbb{R}$. We will sometimes express the Leibniz completeness as $\mathcal{F}(^*\mathbb{K})=\mu(\mathbb{K})$ (Definition~\ref{D: Infinitesimals, etc.}) which is equivalent to $\mathcal{F}(^*\mathbb{K})/\mathcal{I}(^*\mathbb{K})=\mathbb{K}$ (Theorem~\ref{T: Maximal Ideal}).

	\item \emph{Cantor $\kappa$-completeness}, monotone completeness, Weierstrass completeness, Bolzano completeness and Heine-Borel completeness typically appear in real analysis as ``theorems'' or ``important principles'' rather than as forms of completeness; however, in non-standard analysis, Cantor $\kappa$-completeness takes a much more important role along with the concept of algebraic saturation.

	 \item \emph{Cauchy completeness}, listed as number 7 above, is commonly known as \emph{sequential completeness} in the particular case of Archimedean fields (and metric spaces), where $I=\mathbb N$. It has also been used in constructions of the real numbers: Cantor's construction using fundamental (Cauchy) sequences (see Hewitt \& Stromberg~\cite{hewitt} and  O'Connor~\cite{oconnor} and also Borovik \& Katz~\cite{BorovikKatz}).

  \item \emph{Dedekind completeness} was introduced by Dedekind (independently from many others, see O'Connor~\cite{oconnor}) at the end of the $19^\textrm{th}$ century. From the point of view of modern mathematics, Dedekind proved the consistency of the axioms of the real numbers by constructing his field of Dedekind cuts, which is an example of a Dedekind complete totally ordered field.
  
  \item \emph{Hilbert completeness} was originally introduced by Hilbert in 1900 with his axiomatic definition of the real numbers (see Hilbert~\cite{hilbert} and O'Connor~\cite{oconnor}).
  \end{itemize}
\end{remark}
	Here are some commonly known facts about Dedekind completeness.

\begin{theorem}[Existence of Dedekind Fields]\label{T: Existence of Dedekind Fields}
  There exists a Dedekind complete field.
\end{theorem}

\begin{proof} For the classical constructions of such fields due to Dedekind and Cantor, we refer the reader to  Rudin~\cite{poma} and Hewitt \& Stromberg~\cite{hewitt}, respectively. For a more recent proof of the existence of a Dedekind complete field (involving the axiom of choice) we refer to Banaschewski~\cite{bana} and for a non-standard proof of the same result we refer to Hall \& Todorov~\cite{HallTodDedekind11}.
\end{proof}




\begin{theorem}\label{T: Embedding}
  Let $\mathbb{A}$ be an Archimedean field and $\mathbb{D}$ be a Dedekind complete field. For every  $\alpha\in\mathbb{A}$ we let $C_\alpha=:\{q\in\mathbb{Q}: q<\alpha\}$. Then for every $\alpha,\beta\in\mathbb{A}$ we have: (i) $\sup_\mathbb{D}(C_{\alpha+\beta})=\sup_\mathbb{D}(C_\alpha)+\sup_\mathbb{D}(C_\beta)$.; (ii) $\sup_\mathbb{D}(C_{\alpha\beta})=\sup_\mathbb{D}(C_\alpha)\sup_\mathbb{D}(C_\beta)$; (iii) $\alpha\leq\beta$ implies $C_\alpha\subseteq C_\beta$. Consequently, the mapping $\sigma:\mathbb{A}\to\mathbb{D}$, given by $\sigma(\alpha)=:\sup_\mathbb{D}(C_\alpha)$, is an order field embedding of $\mathbb{A}$ into $\mathbb{D}$.  
\end{theorem}
	
\begin{corollary}\label{C: ded order iso}
  All Dedekind complete fields are mutually order-isomorphic and they have the same cardinality, which is usually denoted by $\mathfrak c$. Consequently,  every Archimedean field has cardinality at most $\mathfrak c$.
\end{corollary}

\begin{theorem}\label{T: Dedekind} Every Dedekind complete totally ordered field is Archimedean.
\end{theorem}

\begin{proof}
  Let $\mathbb{D}$ be such a field and suppose, to the contrary, that $\mathbb{D}$ is non-Archimedean. Then  $\mathcal L(\mathbb{D})\not=\varnothing$ by Theorem~\ref{T: Archimedean Property}. Thus $\mathbb{N}\subset\mathbb{D}$ is bounded from above by $|\lambda|$ for any $\lambda\in\mathcal L(\mathbb D)$ so that $\alpha=\sup_\mathbb D(\mathbb N)\in\mathbb{K}$ exists. Then there exists $n\in\mathbb{N}$ such that $\alpha-1< n$ implying $\alpha< n+1$, a contradiction.
\end{proof}

\section{Completeness of an Archimedean Field}\label{S: Completeness of an Archimedean Field}

	We show that in the particular case of an Archimedean field, the different forms of completeness (1)-(10) in Definition~\ref{D: Completeness of a Totally Ordered Field} are equivalent and each of them characterizes the field of real numbers. The reader who is interested in even more comprehensive characterization of the field of reals might consult also with Propp~\cite{jPropp} and  Teismann~\cite{hTeismann2013}. In the case of a non-Archimedean field, the equivalence of these different forms of completeness fails to hold -- we shall discuss this in the next section.

\begin{theorem}[Completeness of an Archimedean Field]\label{T: Completeness of an Archimedean Field} Let $\mathbb{K}$ be a totally ordered Archimedean field. Then the following are equivalent. 
  \begin{T-enum}
   \item $\mathbb{K}$ is Cantor $\kappa$-complete for all infinite cardinal $\kappa$.
     
   \item $\mathbb{K}$ is Leibniz complete.

   \item $\mathbb K$ is Heine-Borel complete.
                     
   \item $\mathbb{K}$ is monotone complete.
                  
   \item $\mathbb{K}$ is Cantor complete (i.e. Cantor $\aleph_1$-complete, not necessarily for all cardinals).
                  
   \item $\mathbb{K}$ is Weierstrass complete.
   
   \item $\mathbb{K}$ is Bolzano complete.
                  
   \item $\mathbb{K}$ is Cauchy complete.
                  
   \item $\mathbb{K}$ is Dedekind complete.

   \item $\mathbb{K}$ is Hilbert complete.
  \end{T-enum}
\end{theorem}
 
\begin{proof}
  \mbox{} 
  \begin{description}
  \item[$(i)\Rightarrow(ii)$] Let $\kappa$ be the successor of $\card(\mathbb{K})$. Let $x\in\mathcal F(^*\mathbb K)$ and $S=:\{[a,b]:a,b\in\mathbb K\emph{ and } a\le x\le b\textrm{ in }{^*\mathbb K}\}$. Clearly $S$ satisfies the finite intersection property and $\card(S)=\card(\mathbb{K}\times\mathbb{K})=\card(\mathbb{K})<\kappa$; thus, by assumption, there exists $r\in \bigcap_{[a,b]\in S} [a,b]$. To show $x-r\in\mathcal I(^*\mathbb K)$, suppose (to the contrary) that $\frac{1}{n}<|x-r|$ for some $n\in\mathbb N$. Then either $x<r-\frac{1}{n}$ or $r+\frac{1}{n}<x$. Thus (after letting $r-\frac{1}{n}=b$ or $r+\frac{1}{n}=a$) we conclude that either $r\le r-\frac{1}{n}$, or $r+\frac{1}{n}\le r$, a contradiction. 

 \item[$(ii)\Rightarrow(iii)$] Our assumption (ii) justifies the following definitions: We define $\st: \mathcal{F}(^*\mathbb K)\to\mathbb K$ by $\st(x)=r$ for $x=r+dx$, $dx\in\mathcal I({^*\mathbb K})$. Also, if $S\subset\mathbb K$, we let $\st[^*S]=\{\st(x): x\in{^*S}\cap\mathcal{F}(^*\mathbb K)\}$.  If $S$ is compact, then $S$ is bounded and closed since $\mathbb K$ is a Hausdorff space as an ordered field. Conversely, if $S$ is bounded and closed, it follows that $^*S\subset\mathcal{F}(^*\mathbb K)$ (Davis~\cite{davis}, p. 89) and $\st[^*S]=S$ (Davis~\cite{davis}, p. 77), respectively. Thus $^*S\subset\mu(S)$, i.e. $S$ is compact (Davis~\cite{davis}, p. 78). 
 
  \item[$(iii)\Rightarrow(iv)$] Let $(x_n)$ be a bounded from above strictly increasing sequence in $\mathbb K$ and let $A=\{x_n\}$ denote the range of the sequence. Clearly $\overline A\setminus A$ is either empty or contains a single element which is the limit of $(a_n)$; hence it suffices to show that $\overline A\neq A$. To this end, suppose, to the contrary, that $\overline A=A$. Then we note that $A$ is compact by assumption since $(a_n)$ is bounded; however, if we define $(r_n)$ by $r_1=1/2(x_2 - x_1)$, $r_n=\min\{r_1,\ldots, r_{n-1}, 1/2(x_{n+1} - x_n)\}$, then we observe that the sequence of open intervals $(U_n)$, defined by $U_n = (x_n-r_n, x_n+r_n)$, is an open cover of $A$ that has no finite subcover. Indeed, $(U_n)$ is pairwise disjoint so that every finite subcover contains only a finite number of terms of the sequence. The latter contradicts the compactness of $A$. 
 
  \item[$(iv)\Rightarrow(v)$] Suppose that $\{[a_i,b_i]\}_{i\in\mathbb{N}}$ satisfies the finite intersection property. Let $\Gamma_n=:\cap_{i=1}^n[a_i,b_i]$ and observe that $\Gamma_n=[\alpha_n, \beta_n]$ where $\alpha_n=:\max_{i\le n} a_i$ and $\beta_n=:\min_{i\le n}b_i$. Then $\{\alpha_n\}_{n\in\mathbb N}$ and $\{-\beta_n\}_{n\in\mathbb N}$ are bounded increasing sequences; thus $\alpha=:\lim_{n\to\infty}\alpha_n$ and $-\beta=:\lim_{n\to\infty}-\beta_n$ exist by assumption. If $\beta<\alpha$, then for some $n$ we would have $\beta_n<\alpha_n$, a contradiction; hence, $\alpha\le\beta$. Therefore $\cap_{i=1}^{\infty}[a_i,b_i]=[\alpha,\beta]\neq\varnothing$.

  \item[$(v)\Rightarrow(vi)$] This is the familiar \emph{Bolzano-Weierstrass Theorem} (Bartle \& Sherbert~\cite{bartle}, p. 79). 

 \item[$(vi)\Rightarrow(vii)$] Let $A\subset \mathbb{K}$ be a bounded infinite set. By the Axiom of Choice, $A$ has a denumerable subset -- that is, there exists an injection $\{x_n\}:\mathbb{N}\to A$. As $A$ is bounded, $\{x_n\}$ has a subsequence $\{x_{n_k}\}$ that converges to a point $x\in\mathbb{K}$ by assumption. Then $x$ must be a cluster point of $A$ because the sequence $\{x_{n_k}\}$ is injective, and thus not eventually constant.

  \item[$(vii)\Rightarrow(viii)$] For the index set we can assume that $I=\mathbb N$ since cofinality of any Archimedean set is $\aleph_0=\card(\mathbb N)$. Let $\{x_n\}$ be a Cauchy sequence in $\mathbb{K}$. Then $\mathrm{range}(\{x_n\})$ is a bounded set. If $\mathrm{range}(\{x_n\})$ is finite, then $\{x_n\}$ is eventually constant (and thus convergent). Otherwise, $\mathrm{range}(\{x_n\})$ has a cluster point $L$ by assumption. To show that $\{x_n\}\to L$, let $\epsilon\in\mathbb{K}_+$ and $N\in\mathbb{N}$ be such that $n,m\ge N$ implies that $|x_n-x_m|<\frac{\epsilon}{2}$. Observe that the set $\{n\in\mathbb{N} : |x_n-L|<\frac{\epsilon}{2} \}$ is infinite because $L$ is a cluster point, so that $A=:\{n\in\mathbb{N} : |x_n-L|<\frac{\epsilon}{2}, n\ge N\}$ is non-empty. Let $M=:\min A$. Then, for $n\ge M$, we have $|x_n-L|\le|x_n-x_M|+|x_M-L|<\epsilon$, as required.
  
  \item[$(viii)\Rightarrow(ix)$] This proof can be found in (Hewitt \& Stromberg~\cite{hewitt}, p. 44).

  \item[$(ix)\Rightarrow(x)$] Let $\mathbb{A}$ be a totally ordered Archimedean field extension of $\mathbb{K}$. We have to show that $\mathbb{A}=\mathbb{K}$. Recall that $\mathbb{Q}$ is dense in $\mathbb{A}$ as it is Archimedean; hence, the set $\{q\in \mathbb{Q} : q<a\}$ is non-empty and bounded from above in $\mathbb{K}$ for all $a\in\mathbb{A}$. Consequently, the mapping 
$\sigma:\mathbb{A}\to\mathbb{K}$, where $\sigma(a)=:\sup_\mathbb{K}\{q\in\mathbb{Q} : q<a\}$, is well-defined by our assumption. Note that $\sigma$ fixes $\mathbb{K}$. To show that $\mathbb{A}=\mathbb{K}$ we will show that $\sigma$ is just the identity map. Suppose (to the contrary) that $\mathbb{A}\neq\mathbb{K}$ and let $a\in\mathbb{A}\setminus\mathbb{K}$. Then $\sigma(a)\neq a$ so that either $\sigma(a)>a$ or $\sigma(a)<a$. If it is the former, then there exists $p\in\mathbb{Q}$ such that $a<p<\sigma(a)$, contradicting the fact that $\sigma(a)$ is the \emph{least} upper bound for $\{q\in\mathbb{Q} : q<a\}$ and if it is the latter then there exists $p\in\mathbb{Q}$ such that $\sigma(a)<p<a$, contradicting the fact that $\sigma(a)$ is an upper bound for $\{q\in\mathbb{Q} : q<a\}$.  
    
    
    

  \item[$(x)\Rightarrow(i)$]  Let $\mathbb{D}$ be a Dedekind complete field (such a field exists by Theorem~\ref{T: Existence of Dedekind Fields}). We can assume that $\mathbb{K}$ is an ordered subfield of $\mathbb{D}$ by Theorem~\ref{T: Embedding}. Thus we have $\mathbb{K}=\mathbb{D}$ by assumption, since $\mathbb D$ is Archimedean. Now suppose, to the contrary, that there is an infinite cardinal $\kappa$ and a family $[a_i,b_i]_{i\in I}$ of fewer than $\kappa$ closed bounded intervals in $\mathbb K$ with the finite intersection property such that $\bigcap_{i\in I}[a_i,b_i]=\varnothing$.  Because $[a_i,b_i]$ satisfies the finite intersection property, the set $A=:\{a_i :i\in I\}$ is bounded from above. Indeed, for any $i\in I$, if there were a $j\in I$ such that $a_j>b_i$ then $[a_j,b_j]\cap [a_i,b_i]=\varnothing$ contradicting the F.I.P., thus $b_i$ is an upper bound of $A$. As well, $A$ is non-empty so that $c=:\sup(A)$ exists in $\mathbb{D}$, and $a_i\le c\le b_i$ for all $i\in I$ so that $c\in\mathbb{D}\setminus\mathbb{K}$. Therefore $\mathbb{D}$ is a proper field extension of $\mathbb{K}$, a contradiction.
\end{description}
\end{proof}
\begin{remark}
  It should be noted that the equivalence of $(ii)$ and $(ix)$ above is proved in Keisler (\cite{jKeislerF}, p. 17-18) with somewhat different arguments. Also, the equivalence of $(ix)$ and $(x)$ is proved in Banaschewski~\cite{bana} using a different method than ours (with the help of the axiom of choice).
\end{remark}


\section{Completeness of a Non-Archimedean Field}\label{S: Completeness of a Non-Archimedean Field}

In this section, we discuss how removing the assumption that $\mathbb K$ is Archimedean affects our result from the previous section. In particular, several of the forms of completeness listed in Definition~\ref{D: Completeness of a Totally Ordered Field} no longer hold, and those that do are no longer equivalent. 

\begin{theorem}\label{T: completeness -> archimedean}
   Let $\mathbb K$ be an ordered field satisfying any of the following:
   \begin{T-enum}
      \item Bolzano completeness.
      \item Weierstrass completeness.
      \item Monotone completeness.
      \item Dedekind completeness
      \item Cantor $\kappa$-completeness for $\kappa>\card(\mathbb K)$.
      \item Leibniz completeness (in the sense that every finite number can be decomposed \emph{uniquely} into the sum of an element of $\mathbb K$ and an infinitesimal).
   \end{T-enum}
 Then $\mathbb K$ is Archimedean. Consequently, if $\mathbb K$ is non-Archimedean, then each of (i)-(vi) is false. 
\end{theorem}
\begin{proof}
   We will only prove the case for Leibniz completeness and leave the rest to the reader.

  Suppose, to the contrary, that $\mathbb K$ is non-Archimedean. Then there exists a $dx\in\mathcal I(\mathbb K)$ such that $dx\neq0$ by Theorem~\ref{T: Archimedean Property}. Now take $\alpha\in\mathcal F(^*\mathbb K)$ arbitrarily. By assumption there exists unique $k\in\mathbb K$ and $d\alpha\in\mathcal I(^*\mathbb K)$ such that $\alpha=k+d\alpha$. However, we know that $dx\in\mathcal I(^*\mathbb K)$ as well because $\mathbb{K}\subset{^*\mathbb{K}}$ and the ordering in $^*\mathbb{K}$ extends that of $\mathbb{K}$. Thus $(k+dx)+(d\alpha-dx)=k+d\alpha=\alpha$ where $k+dx\in\mathbb K$ and $d\alpha-dx\in\mathcal I(^*\mathbb K)$. This contradicts the uniqueness of $k$ and $d\alpha$. Therefore $\mathbb K$ is Archimedean.
\end{proof}

Recall that $\kappa^+$ stands for the successor of $\kappa$, $\aleph_1=\aleph_0^+$ and $\aleph_0=\card(\mathbb N)$.

\begin{theorem}[Cardinality and Cantor Completeness]\label{T: Cardinality and Cantor Completeness}
  Let $\mathbb K$ be an ordered field. If $\mathbb K$ is non-Archimedean and Cantor $\kappa$-complete (see Definition~\ref{D: Completeness of a Totally Ordered Field}), then $\kappa\le\card(\mathbb K)$.
\end{theorem}
\begin{proof}
   This is essentially the proof of $(i)\Rightarrow(ii)$ in Theorem~\ref{T: Completeness of an Archimedean Field}.
  
\end{proof}

	The next result (unpublished) is due to Hans Vernaeve.

\begin{theorem}[Cofinality and Saturation]\label{T: Cofinality and Saturation}
  Let $\mathbb K$ be an ordered field and $\kappa$ be an uncountable cardinal. Then the following are equivalent:
  \begin{T-enum}
    \item $\mathbb K$ is algebraically $\kappa$-saturated.
    \item $\mathbb K$ is Cantor $\kappa$-complete and $\kappa\leq\cof(\mathbb K)$.
  \end{T-enum}
\end{theorem}
\begin{proof}
  \mbox{}
  \begin{description}
    \item[$(i)\Rightarrow(ii)$] Let $\mathcal C=:\{[a_{\gamma},b_{\gamma}]\}_{\gamma\in \Gamma}$ and $\mathcal O=:\{(a_{\gamma}, b_{\gamma})\}_{\gamma\in \Gamma}$ be families of fewer than $\kappa$ bounded closed and open intervals, respectively, where $\mathcal C$ has the finite intersection property. If $a_k=b_p$ for some $k,p\in\Gamma$, then  $\bigcap_{\gamma\in \Gamma}[a_{\gamma},b_{\gamma}]=\{a_k\}$ by the finite intersection property in $\mathcal C$. Otherwise, $\mathcal O$ has the finite intersection property; thus, there exists $\alpha\in\bigcap_{\gamma\in \Gamma} (a_{\gamma}, b_{\gamma})\subseteq\bigcap_{\gamma\in \Gamma}[a_{\gamma}, b_{\gamma}]$ by algebraic $\kappa$-saturation. Hence $\mathbb K$ is Cantor $\kappa$-complete. To show that the cofinality of $\mathbb K$ is greater than or equal to $\kappa$, let $A\subset\mathbb K$ be a set with $\card(A)<\kappa$. Then $\bigcap_{a\in A}(a,\infty)\neq\emptyset$ by algebraic $\kappa$-saturation.

    \item[$(ii)\Rightarrow(i)$] Let $\{(a_{\gamma},b_{\gamma})\}_{\gamma\in \Gamma}$ be a family of fewer than $\kappa$ open intervals with the finite intersection property. Without loss of generality, we can assume that each interval is bounded. As $\cof(\mathbb K)\ge\kappa$, there exists $\frac{1}{\rho} \in \ub(\{ \frac{1}{b_l -a_k} : l, k\in \Gamma \})$ (that is, $\frac{1}{b_l-a_k}\le\frac{1}{\rho}$ for all $l,k\in \Gamma$) which implies that $\rho>0$ and that $\rho$ is a lower bound of $\{b_l-a_k : l, k\in \Gamma\}$. Next, we show that the family $\{[a_\gamma+\frac{\rho}{2},b_\gamma-\frac{\rho}{2}]\}_{\gamma\in\Gamma}$ satisfies the finite intersection property. Let $\gamma_1,\ldots,\gamma_n\in\Gamma$ and $\zeta=:\max_{k\le n}\{a_{\gamma_k} + \frac{\rho}{2}\}$. Then, for all $m\in\mathbb N$ such that $m\le n$, we have $a_{\gamma_m} + \frac{\rho}{2}\le \zeta \le b_{\gamma_m} - \frac{\rho}{2}$ by the definition of $\rho$; thus, $\zeta\in[a_{\gamma_m}+\frac{\rho}{2}, b_{\gamma_m}-\frac{\rho}{2}]$ for $m\le n$. By Cantor $\kappa$-completeness, there exists $\alpha\in\bigcap_{\gamma\in\Gamma} [a_{\gamma}+\frac{\rho}{2}, b_{\gamma}-\frac{\rho}{2}]\subseteq\bigcap_{\gamma\in\Gamma}(a_{\gamma},b_{\gamma})$.
  \end{description}
\end{proof}


\begin{lemma}\label{L: sat -> seq}
  Let $\mathbb K$ be an ordered field. If $\mathbb K$ is algebraically $\aleph_1$-saturated, then $\mathbb K$ is sequentially complete.
\end{lemma}
\begin{proof}
   Let $\{x_n\}$ be a Cauchy sequence in $\mathbb K$. Define $\{\delta_n\}$ by $\delta_n=|x_n-x_{n+1}|$. If $\{\delta_n\}$ is not eventually zero, then there is a subsequence $\{\delta_{n_k}\}$ such that $\delta_{n_k}>0$ for all $k$; however, this yields $\bigcap_k (0,\delta_{n_k})\neq\varnothing$, which contradicts $\delta_n\to 0$. Therefore $\{\delta_n\}$ is eventually zero so that $\{x_n\}$ is eventually constant.
\end{proof}

\begin{lemma}\label{L: cantor -> sequential}
  Let $\mathbb K$ be a Cantor complete ordered field which is not algebraically saturated. Then $\mathbb K$ is sequentially complete.
\end{lemma}
\begin{proof}
   By Theorem~\ref{T: Cofinality and Saturation}, we know there exists an unbounded increasing sequence $\{\frac{1}{\epsilon_n}\}$. Let $\{x_n\}$ be a Cauchy sequence in $\mathbb K$. For all $n\in\mathbb N$, we define $S_n=:[x_{m_n} - \epsilon_n, x_{m_n} + \epsilon_n]$, where $m_n\in\mathbb N$ is the minimal element such that $l,j\ge m_n$ implies $|x_l-x_j|<\epsilon_n$. Let $A\subset \mathbb N$ be finite and $\rho=:\max(A)$; then we observe that $x_{m_{\rho}}\in S_k$ for any $k\in A$ because $m_k\le m_{\rho}$; hence $\{S_n\}$ satisfies the finite intersection property. Therefore there exists $L\in\bigcap_{k=1}^{\infty}S_k$ by Cantor completeness. It then follows that $x_n\to L$ since $\{\epsilon_n\}\to0$.
\end{proof}

\begin{theorem}\label{T: non-arch completeness}
   Let $\mathbb K$ be an ordered field, then we have the following implications
   \begin{align*}
      \mathbb K\textrm{ is algebraically }\kappa\textrm{-saturated}
      &\Rightarrow \mathbb K \textrm{ is Cantor } \kappa\textrm{-complete}\\
      &\Rightarrow \mathbb K \textrm{ is sequentially complete.}
   \end{align*}
\end{theorem}
\begin{proof}
   The first implication follows from Theorem~\ref{T: Cofinality and Saturation}. For the second we have two cases depending on whether $\mathbb K$ is algebraically saturated, which are handled by Lemmas~\ref{L: sat -> seq} and Lemma~\ref{L: cantor -> sequential}.
\end{proof}

The next two results require the generalized continuum hypothesis (GCH) in the form $2^\kappa=\kappa^+$, where $\kappa$ is a cardinal number.

\begin{theorem}[First Uniqueness Result]\label{T: First Uniqueness Result} All real closed fields (Lang~\cite{lang}, p. 451) of the same cardinality which are algebraically saturated (Definition~\ref{D: Completeness of a Totally Ordered Field}) are isomorphic. 
\end{theorem}
\begin{proof} We refer to Erd\"{o}s \&  Gillman \& Henriksen~\cite{ErdGillHenr55}
(for a presentation see also: Gillman \& Jerison~\cite{lFux63}, p. 179-185).
\end{proof}

\begin{theorem}[Second Uniqueness Result] \label{T: Second Uniqueness Result} 	Let $\kappa$ be an infinite cardinal and $\mathbb K$ be a totally ordered field with the following properties:
\begin{T-enum}

\item $\card(\mathbb K)=\kappa^+$.

\item $\mathbb K$ is a real closed field (Lang~\cite{lang}, p. 451).

\item $\mathbb K$ is Cantor complete (Definition~\ref{D: Completeness of a Totally Ordered Field}).

\item $\mathbb K$ contains $\mathbb R$ as a subfield.

\item $\mathbb K$ admits an infinitesimal scale, i.e. there exists a positive infinitesimal $s$ in $\mathbb K$ such that the sequence $(s^{-n})$ is unbounded (from above). 

\end{T-enum}
Then $\mathbb K$ is unique up to field isomorphism.
\end{theorem}
\begin{proof} We refer to Todorov \& Wolf~\cite{TodWolf04} (where $\mathbb K$ appears as $^\rho\mathbb R$). For a presentation see also (Todorov~\cite{tdTodAxioms10}, Section 3). 
\end{proof} 
	Notice that (iv) and (v) imply that $\mathbb R$ is a proper subfield of $\mathbb K$ and that $\mathbb K$ is non-saturated. 


\section{Infinitesimals in Algebra and Non-Standard Analysis}\label{S: Infinitesimals in Algebra and Non-Standard Analysis}

	In this section we present several examples of non-Archimedean fields -- some constructed in the framework of algebra, others in non-standard analysis. On one hand, these examples illustrate some of the results from the previous sections, but on the other hand, they prepare us for the discussion of the history of calculus in the next section. 

	The examples of non-Archimedean fields constructed in the framework of algebra (including our earlier Example~\ref{Ex: Field of Rational Functions}) shows that the concept of \emph{infinitesimal} is not exclusively associated with non-standard analysis -- \textbf{infinitesimals are everywhere around us} -- if only you ``really want to open your eyes and to see them''. In particular, every totally ordered field containing a proper copy of $\mathbb R$ contains non-zero infinitesimals.


This section alone -- with the help perhaps, of Section~\ref{S: Preliminaries: Ordered Rings and Fields} -- might be described as ``the shortest introduction to non-standard analysis ever written'' and for some readers might be an ``eye opener.'' 

	If $X$ and $Y$ are two sets, we denote by $Y^X$ the set of all functions from $X$ to $Y$. In particular, $Y^\mathbb N$ stands for the set of all sequences in $Y$. We use the notation $\mathcal{P}(X)$ for the power set of $X$. To simplify the following discussion, we shall adopt the GCH (Generalized Continuum Hypothesis) in the form $2^{\kappa}=\kappa_+$ for any cardinal number $\kappa$. Also, we let $\card(\mathbb N)=\aleph_0$ and $\card(\mathbb R) =\frak{c}$ for the successor of $\aleph_0$ and ${\frak{c}^+}$ for the successor of $\frak{c}$. 

In what follows, $\mathbb{K}$ is a totally ordered field (Archimedean or not) with cardinality $\card(\mathbb K)=\kappa$ and cofinality ${\rm cof}(\mathbb K)$ (Definition~\ref{D: Totally Ordered Rings}). Most of the results in this section remain true if the field $\mathbb K$ is replaced by $\mathbb K(i)$. Recall that $\mathbb K$ is a real closed field (Lang~\cite{lang}, p. 451) if and only if $\mathbb K(i)$ is an algebraically closed field (Lang~\cite{lang}, p. 272) by Artin \& Schreier~\cite{ArtinSchreier27}. 

	We shall focus of the following field extensions:

 \begin{equation}\label{E: Chain 1}
\mathbb K\subset \mathbb K(t)\subset \mathbb K\bra t^{\mathbb Z}\ket\subset\mathbb K\{\{t\}\}\subset \mathbb K\langle t^{\mathbb R}\rangle\subset \mathbb K((t^{\mathbb R})),
\end{equation}
where (in backward order):
\begin{examples}[Power Series]\label{Ex: Power Series}
\begin{Ex-enum}

\item The field of \emph{Hahn power series with coefficients in $\mathbb K$ and valuation group} $\mathbb R$ (Hahn~\cite{hHahn}) is defined to be the set 
\[
\mathbb K((t^{\mathbb R}))=: \Big\{S=\sum_{r\in\mathbb R} a_rt^r : a_r\in\mathbb K\emph{ and } \supp(S) \emph{ is a well ordered set}\Big\},
\]
where $\supp(S)=\{r\in\mathbb R: a_r\not=0\}$. We supply $\mathbb K((t^{\mathbb R}))$ (denoted sometimes by $\mathbb K(\mathbb R)$) with the usual polynomial-like addition and multiplication and the \emph{canonical valuation} $\nu:\mathbb K((t^{\mathbb R}))\to\mathbb R\cup\{\infty\}$ defined by $\nu(0)=:\infty$ and $\nu(S)=:\min(\supp(S))$ for all $S\in\mathbb K((t^{\mathbb R})), S\not= 0$. In addition, $\mathbb K((t^{\mathbb R}))$ has a natural ordering given by 
\[
\mathbb K((t^{\mathbb R}))_+=:\Big\{S=\sum_{r\in\mathbb R} a_rt^r : a_{\nu(S)}>0\Big\}.
\]

\item The field of \emph{Levi-Civit\'{a} power series} (Levi-Civit{\'a}~\cite{LC}) is defined to be the set 
\[
\mathbb K\langle t^{\mathbb R}\rangle=:\Big\{\sum_{n=0}^{\infty}a_nt^{r_n} : a_n\in\mathbb K \emph{ and } r_n\in\mathbb R, r_0<r_1<\dots\to\infty\Big\},
\]
where $r_0<r_1<\dots\to\infty$ means that $(r_n)$ is a unbounded strictly increasing sequence in $\mathbb R$.
\item The field of \emph{Puiseux power series}  with coefficients in $\mathbb K$ (called also \emph{Newton-Puiseux series}) is 
\[
\mathbb K\{\{t\}\}=:\Big\{\sum_{n=m}^\infty a_n\, t^{n/\nu}: a_n\in\mathbb K \text{ and } m\in\mathbb Z, \nu\in\mathbb N\Big\}.
\]
\item $\mathbb K\bra t^{\mathbb Z}\ket=:\Big\{\sum_{n=m}^{\infty}a_nt^n : a_n\in\mathbb K \emph{ and }m\in\mathbb Z\Big\}$ is the field of the \emph{Laurent power series} with coefficients in $\mathbb K$.

\item $\mathbb K(t)$ is the field of rational functions with coefficients in $\mathbb K$ (Example~\ref{Ex: Field of Rational Functions}).
\end{Ex-enum}
\end{examples}
The fields $\mathbb K\bra t^{\mathbb Z}\ket$, $\mathbb K\{\{t\}\}$ and $\mathbb K\langle t^{\mathbb R}\rangle$ are supplied with algebraic operations, ordering and valuation inherited from $\mathbb K((t^{\mathbb R}))$. As the ordering of $\mathbb K(t)$ given in Example~\ref{Ex: Field of Rational Functions} agrees with the ordering inherited from $\mathbb K( (t^\mathbb R))$, it follows that each of the fields listed above are also non-Archimedean. To illustrate this last fact, we consider the elements $\sum_{n=0}^{\infty}n!\, t^{n+1/3}$ and $\sum_{n=-1}^{\infty} t^{n+1/2}=\frac{\sqrt{t}}{t-t^2}$ of $\mathbb K\bra t^\mathbb R\ket$, which are examples of positive infinitesimal and positive infinitely large numbers, respectively.

\begin{remark}[A Generalization]  The valuation group $\mathbb R$ in $t^\mathbb R$ can be replaced by any ordered divisible Abelian group $(G, +, <)$ (often $(\mathbb Z, +, <)$, $(\mathbb Q, +, <)$ or $(\mathbb R, +, <)$). The result are the fields: $\mathbb K((t^G))$ (often denoted by $\mathbb K(G)$), $\mathbb K((t^\mathbb Q))$, $\mathbb K\bra t^{G}\ket$, $\mathbb K\bra t^{\mathbb Z}\ket$, $\mathbb K\bra t^{\mathbb Q}\ket$, etc. 
\end{remark}

If $\mathbb K$ is real closed or algebraically closed (Lang~\cite{lang}, p. 451, 272), then $\mathbb K\{\{t\}\}$, $\mathbb K\langle t^{\mathbb R}\rangle$ and $\mathbb K((t^{\mathbb R}))$ are also real closed or algebraically closed, respectively. Consequently, the fields $\mathbb K$, $\mathbb K\{\{t\}\}$, $\mathbb K\bra t^\mathbb R\ket$, $\mathbb K((t^\mathbb R))$ and $^*\mathbb K$ (see below) share the property to be \emph{real closed} or \emph{algebraically closed}. In particular, $\mathbb R\{\{t\}\}$ is the real closure of $\mathbb R\bra t^{\mathbb Z}\ket$ and $\mathbb R\bra t^{\mathbb Q}\ket$ is the completion of $\mathbb R\{\{t\}\}$  relative the the valuation metric $|\cdot|_v$. Similarly, $\mathbb C\{\{t\}\}$ is the algebraic closure of $\mathbb C\bra t^{\mathbb Z}\ket$ and $\mathbb C\bra t^{\mathbb Q}\ket$ is the completion of $\mathbb C\{\{t\}\}$  relative the the valuation metric $|\cdot|_v$.  For more detail we refer to (Hahn~\cite{hHahn}, Ostrowski~\cite{aOstrowski}, Prestel~\cite{aPrestel}, Robinson~\cite{aRob66}-\cite{aRob73}, Lightstone \& Robinson~\cite{LiRob}). Furthermore, the cofinality of each of the fields $\mathbb K\bra t^{\mathbb Z}\ket$, $\mathbb K\langle t^{\mathbb R}\rangle$, and $\mathbb K((t^{\mathbb R}))$ is $\aleph_0=\card(\mathbb N)$ because the sequence $(1/t^n)_{n\in\mathbb N}$ is unbounded in each of them. The field $\mathbb{K}((t^{\mathbb{R}}))$ is spherically complete (Hahn~\cite{hHahn}, Krull~\cite{krull} and Luxemburg~\cite{wLux76}, Theorem~2.12). Consequently, the fields  $\mathbb K\bra t^{\mathbb Z}\ket$, $\mathbb K\langle t^{\mathbb R}\rangle$, and $\mathbb K((t^{\mathbb R}))$ are Cauchy (and sequentially) complete; however, none of these fields are necessarily Cantor complete or saturated. In particular, if $\mathbb K$ is Archimedean, these fields are certainly not Cantor complete. The fact that the fields $\mathbb{R}(t^{\mathbb Z})$ and $\mathbb{R}\langle t^{\mathbb R}\rangle$ are sequentially complete was also proved independently in (Laugwitz~\cite{Laugwitz}). The field $\mathbb{R}\langle t^{\mathbb R}\rangle$ was introduced by Levi-Civit\'{a} in \cite{LC} and later was investigated by D. Laugwitz in \cite{Laugwitz} as a potential framework for the rigorous foundation of infinitesimal calculus before the advent of Robinson's nonstandard analysis. It is also an example of a real-closed valuation field that is sequentially complete, but not spherically complete (Pestov~\cite{vPestov}, p. 67).  The field of Puiseux power series $\mathbb K\{\{t\}\}$ is introduced by Isaac Newton in 1676 and later rediscover by Victor Puiseux in 1850. 

Beyond these examples of fields based on formal series, we have the following examples from non-standard analysis.

\begin{definition}[Free Ultrafilter] 
   Recall that a collection $\mathcal{U}$ of subsets of $\mathbb N$ is a \emph{free ultrafilter} on $\mathbb N$ if: (a) $\varnothing\notin\mathcal{U}$; (b) $\mathcal{U}$ is closed under finitely many intersections; (c) If $A\in\mathcal{U}$ and $B\subseteq\mathbb N$, then $A\subseteq B$ implies $B\in\mathcal{U}$; (d) $\bigcap_{A\in\mathcal{U}}\, A=\varnothing$; (e) For every $A\subseteq\mathbb N$ either $A\in\mathcal{U}$, or $\mathbb N\setminus A\in\mathcal{U}$. 
\end{definition}

	Notice that the Fr{\'e}chet free filter $\mathcal F_r=\big\{S\subseteq\mathbb N: \mathbb N\setminus S \text{ is a finite set}\big\}$ on $\mathbb N$ satisfies all properties above except the last one. The existence of free ultrafilters follows from the axiom of choice (Zorn's lemma) as a maximal extension of $\mathcal F_r$. For more details we refer again to (Lindstr\o m~\cite{lindstrom}). Let $\mathcal U$ be one (arbitrarily chosen) ultrafilter on $\mathbb N$. We shall keep $\mathcal U$ fixed in what follows.

\begin{definition}[Non-Standard Field Extension]\label{D: Non-Standard Analysis} Let $\mathbb K^\mathbb N$ be the ring of sequences in $\mathbb K$ and $\sim$ is an equivalence relation on $\mathbb K^\mathbb N$ defined by: $(a_n)\sim (b_n)$ if $\{n\in \mathbb N: a_n=b_n\}\in\mathcal{U}$. The the factor space $^*\mathbb K=\mathbb K^{\mathbb N}/{\sim}$ is called a \emph{non-standard extension}of $\mathbb K$.   We denote by $\bra a_n\ket\in{^*\mathbb K}$ the equivalence class of the sequence $(a_n)\in{\mathbb K^\mathbb N}$. The original field $\mathbb K$ is embedded as a subfield of $^*\mathbb K$ by mean of the constant sequences: $r\to\bra r, r,\dots\ket$, where $r\in\mathbb R$. More generally, the \emph{non-standard extension} of a set $S\subseteq\mathbb K$ is defined by $^*S=\big\{\bra a_n\ket\in{^*\mathbb K}: \{n\in \mathbb N: a_n\in S\}\in\mathcal{U}\big\}$. Let $X\subseteq\mathbb K$ and $f: X\to\mathbb K$ be a function. We defined its \emph{non-standard extension} $^*f: {^*X}\to{^*\mathbb K}$ of $f$ by the formula $^*f(\bra x_n\ket)=\bra f(x_n)\ket$. It is clear that $^*f\rest X=f$, hence we can sometimes skip the asterisks to simplify our notation. Similarly we define $^*f$ for functions $f: X\to\mathbb K^q$, where $X\subseteq\mathbb K^p$ (noting that $^*(\mathbb K^p)={(^*\mathbb K)^p}$). Also if $f\subset \mathbb K^p\times \mathbb K^q$ is a function, then $^*f\subset{^*\mathbb K^p}\times{^*\mathbb K^q}$ is a function as well.   For the details and missing proofs of this and other results we refer to any of the many excellent introductions to non-standard analysis, e.g.  Lindstr\o m~\cite{lindstrom}, Davis~\cite{davis}, Capi\'{n}ski \& Cutland ~\cite{CapinskiCutland95} and Cavalcante~\cite{cavalcante}.
\end{definition}


It turns out that $^*\mathbb K$ is an algebraically saturated ($\frak{c}$-saturated) ordered field extension of $\mathbb K$. The latter implies $\frak{c}\leq\card(^*\mathbb K)$ by Theorem~\ref{T: Cardinality and Cantor Completeness} and $\frak{c}\leq{\rm cof}(^*\mathbb K)$ by Theorem~\ref{T: Cofinality and Saturation}. It can be proved that $^*\mathbb N$ is unbounded from above in $^*\mathbb K$, i.e. $\bigcap_{n\in{^*\mathbb N}}(n, \infty)=\varnothing$. The latter implies $\card(^*\mathbb N)\geq\frak{c}$ by the $\frak{c}$-saturation of $^*\mathbb K$ and thus ${\rm cof}(^*\mathbb K)\le\card(^*\mathbb N)$. Finally, $^*\mathbb K$ is real closed (Lang~\cite{lang}, p. 451) if and only if $\mathbb K$ is real closed. Also,  $^*\mathbb K$ is algebraically closed (Lang~\cite{lang}, p. 272) if and only if $\mathbb K$ is algebraically closed.

If $r\in\mathbb K, r\not=0$, then  $\bra 1/n\ket, \bra r+1/n\ket, \bra n\ket$ present examples for positive infinitesimal, finite (but non-infinitesimal) and infinitely large elements in $^*\mathbb K$, respectively. 

	The simplified form of the transfer principe below is due to Keisler~\cite{jKeislerF}.
\begin{theorem}[Keisler Transfer Principle]\label{T: Keisler Transfer Principle} 
   Let $\mathbb K$ be an ordered Archimedean field and $p, q\in\mathbb N$. Then $S$ is the solution set of the system
   \begin{equation}\label{E: System in K}
   \begin{cases}
   f_i(x)=F_i(x), &i=1, 2, \dots, n_1,\\
   g_j(x)\not= G_j(x),&j=1, 2, \dots, n_2,\\
   h_k(x)\leq H_k(x), &k=1, 2, \dots, n_3,
   \end{cases}
   \end{equation}
   if and only if $^*S$ is the solution set of the system of equations and inequalities
   \begin{equation}\label{E: System in *K}
   \begin{cases}
   ^*f_i(x)={^*}F_i(x), &i=1, 2, \dots, n_1,\\
   ^*g_j(x)\not={^*}G_j(x), &j=1, 2, \dots, n_2,\\
   ^*h_k(x)\leq {^*}H_k(x), &k=1, 2, \dots, n_3.
   \end{cases}
   \end{equation}
Here $f_i, F_i, g_j, G_j\subset \mathbb K^p\times \mathbb K^q$ and  $h_k, H_k\subset \mathbb K^p\times \mathbb K$ are functions in $p$-variables and $n_1, n_2, n_3\in\mathbb{N}_0$ (if $n_1=0$, then $f_i(x)=F_i(x)$ will be missing in (\ref{E: System in K}) and similarly for the rest). The quantifier ``for all'' is over $d, p, q$ and all functions involved.
\end{theorem}

\begin{example}[Non-Standard Real Numbers]\label{Ex: Non-Standard Real Numbers} Let  $^*\mathbb R$ be the non-standard extension of $\mathbb R$ (let $\mathbb K=\mathbb R$ in Definition~\ref{D: Non-Standard Analysis}). The elements of $^*\mathbb R$ are known as \emph{non-standard real numbers} (or \emph{hyperreals}). $^*\mathbb R$ is a real closed algebraically saturated ($\frak{c}$-saturated) field in the sense that every nested sequence of open intervals in $^*\mathbb R$ has a non-empty intersection.  Also, $\mathbb R$ is embedded as an ordered subfield of ${^*\mathbb R}$ by means of the constant sequences. We have $\card(^*\mathbb R)=\frak{c}$ and ${\rm cof}(^*\mathbb R)=\frak{c}$. Indeed, in addition to $\frak{c}\leq\card(^*\mathbb R)$ (see above), we have, by the GCH, $\card(^*\mathbb R)\le \card(\mathbb R^\mathbb N)=(2^{\aleph_0})^{\aleph_0}=2^{(\aleph_0)^2}=2^{\aleph_0}=\frak{c}$. Also, in addition to  $\frak{c}\leq{\rm cof}(^*\mathbb R)$ (see above), we have ${\rm cof}(^*\mathbb R)\le\card(^*\mathbb R)=\frak{c}$. Consequently, $^*\mathbb R$ is unique up to a field isomorphism (it does not depend on the particular choice of the ultrafilter $\mathcal U$) by Theorem~\ref{T: First Uniqueness Result}. It should be mentioned that $^*\mathbb R$ is not Cauchy complete: its completion (in terms of fundamental $\frak{c}$-nets instead of sequences) is a real closed saturated field (Keisler \& Schmerl\cite{KeislerSchmerl91} and  Dales \& Woodin~\cite{DalWoodin}). 
\end{example}

	Here are several important results of non-standard analysis:

\begin{theorem}[Leibniz Completeness Principle] $\mathbb R$ is \emph{Leibniz complete} in the sense that every finite number $x\in{^*\mathbb R}$ is infinitely close to some (necessarily unique) number $r\in\mathbb R$ (\# 2 of Definition~\ref{D: Completeness of a Totally Ordered Field}). We define the standard part mapping $\st: \mathcal{F}(^*\mathbb R)\to\mathbb R$ by $\st(x)=r$. 
\end{theorem}

\begin{theorem}[Limit]\label{T: Limit}  Let  $X\subseteq\mathbb R$ and $f: X\to\mathbb R$ be a real function. Let  $r, L\in\mathbb R$. Then:
\begin{T-enum}
\item $r$ is a non-trivial adherent (cluster) point of $X$ if and only if $r+dx\in{^*X}$ for some non-zero infinitesimal $dx\in{^*\mathbb R}$.

\item
$\lim_{x\to r} f(x)  =  L$ if and only if $^*f(r + dx) \approx L$ for all non-zero infinitesimals $dx\in{^*\mathbb R}$ such that $r+dx\in{^*X}$. In the latter case we have $\lim_{x\to r} f(x) = \st(^*f(r + dx))$. 
\end{T-enum}
\end{theorem}

\begin{theorem}[Derivative]\label{T: Derivative}  Let  $r\in X\subseteq\mathbb R$ and $f: X\to\mathbb R$ be a real function.  Then $f$ is differentiable at $r$ if and only if there exists $L\in\mathbb R$ such that $\frac{^*f(r + dx)-f(r)}{dx} \approx L$ for all non-zero infinitesimals $dx\in{^*\mathbb R}$ such that $r+dx\in{^*X}$. The number $L$ is called \emph{derivative} of $f$ at $r$ and denoted by $f^\prime(r)$. That is $\st\big(\frac{^*f(r + dx)-f(r)}{dx}\big) = f^\prime(r)$.
\end{theorem}
	
\quad \quad Notice that the above characterizations of the concept of \emph{limit} and \emph{derivative} involve \emph{only one quantifier} in sharp contrast with the usual $\varepsilon, \delta$-definition of \emph{limit} in the modern real analysis using three non-commuting quantifiers. On the topic of \emph{counting quantifiers} we refer to Cavalcante~\cite{cavalcante}. For the history of the concepts of \emph{limit and standard part mapping (shadow)} we refer the reader to the recent article Bascelli at al~\cite{Katz at al 2014}.

\begin{example}[Robinson's Asymptotic Numbers] Let $\rho$ be a positive infinitesimal in $^*\mathbb{R}$ (i.e. $0<\rho<1/n$ for all $n\in\mathbb N$). We define the sets of non-standard $\rho$-\emph{moderate} and $\rho$-\emph{negligible} numbers by 
  \begin{eqnarray*}
    \mathcal M_{\rho}(^*\mathbb R)&=&\{x\in{^*\mathbb R} : |x|\le \rho^{-m} \emph{ for some } m\in\mathbb N\},\\
    \mathcal N_{\rho}(^*\mathbb R)&=&\{x\in{^*\mathbb R} : |x| < \rho^n \emph{ for all } n\in\mathbb N\},
  \end{eqnarray*}
  respectively. The \emph{Robinson field of real $\rho$-asymptotic numbers} is the factor ring ${^{\rho}\mathbb R}=:\mathcal M_{\rho}(^*\mathbb R)/\mathcal N_{\rho}(^*\mathbb R)$. We denote by $q: \mathcal M_{\rho}(^*\mathbb R)\to {^\rho\mathbb R}$ the quotient mapping and often simply write $\widehat{x}$ instead of $q(x)$.
\end{example}

	 It is not hard to show that $\mathcal M_{\rho}(^*\mathbb R)$ is a convex subring, and $\mathcal N_{\rho}(^*\mathbb R)$ is a maximal convex ideal; thus $^{\rho}\mathbb R$ is an ordered field. Actually, $^\rho\mathbb{R}$ is a real-closed field (Todorov \& Vernaeve~\cite{TodVern08}, Theorem 7.3) that it is Cantor complete (and thus sequentially complete) but not algebraically $\frak{c}$-saturated.  The field $^{\rho}\mathbb R$ was introduced by A. Robinson in (Robinson~\cite{aRob73}) and in (Lightstone \& Robinson~\cite{LiRob}). $^{\rho}\mathbb R$ is also known as \emph{Robinson's valuation field}, because the mapping $v_\rho:{^{\rho}\mathbb R}\to\mathbb R\cup\{\infty\}$ defined by $v_\rho(\widehat{x})=\st(\log_\rho(|x|))$ if $\widehat{x}\not=0$, and $v_\rho(0)=\infty$, is a non-Archimedean valuation. $^{\rho}\mathbb R$ is also spherically complete (Luxemburg~\cite{wLux76}). We sometimes refer to the branch of mathematics related directly or indirectly to Robinson's field $^\rho\mathbb R$  as \emph{non-standard asymptotic analysis}. For a short survey on the topic we refer to the introduction in Todorov \& Vernaeve~\cite{TodVern08} (see also Oberguggenberger \& Todorov~\cite{OberTod98} and Todorov ~\cite{tdTodAxioms10}-\cite{tdTodLightenings15} , where $^\rho\mathbb C={^\rho}\mathbb R(i)$ appears as the field of scalars of an \emph{algebra of generalized functions of Colombeau type}). 

	We should draw attention to the close similarity (both in the construction and terminology) between the Robinson field $^\rho\mathbb R$ and the Christov quasi-field of asymptotic numbers $\mathcal A$ introduced in Christov~\cite{cyChristov74} (see also Christov \& Todorov\cite{ChrTod84} and Todorov~\cite{tdTod81}).


By a result due to Robinson~\cite{aRob73} the field $\mathbb R\langle t^{\mathbb R}\rangle$ can be embedded as an ordered subfield of ${^\rho\mathbb R}$, where the image of $t$ is $\widehat{\rho}$. We shall write this embedding as an inclusion, $\mathbb R\langle t^{\mathbb R}\rangle\subset{^\rho\mathbb R}$. The latter implies the chain of inclusions (embeddings):            
\begin{equation}\label{E: Chain 2}
   \mathbb R\subset \mathbb R(t)\subset \mathbb R\bra t^{\mathbb Z}\ket\subset \mathbb R\langle t^{\mathbb R}\rangle\subset{^\rho\mathbb R}.
\end{equation}
These embeddings explain the name \emph{asymptotic numbers} for the elements of $^\rho\mathbb R$. Recently it was shown that the fields $^*\mathbb R((t^{\mathbb R}))$ and ${^\rho\mathbb R}$ are ordered field isomorphic  (Todorov \& Wolf~\cite{TodWolf04} ). Since $\mathbb R((t^{\mathbb R}))\subset{^*\mathbb R}((t^{\mathbb R}))$, the chain  (\ref{E: Chain 2}) implies two more chains:
\begin{align}
   &\mathbb R\subset \mathbb R(t)\subset \mathbb R\bra t^{\mathbb Z}\ket\subset \mathbb R\langle t^{\mathbb R}\rangle\subset {\mathbb R((t^{\mathbb R}))}\subset{^\rho\mathbb R}, \label{E: Chain 3}\\
   \label{E: Chain 4}
   &{^*\mathbb R}\subset {^*\mathbb R(t)}\subset{^*\mathbb R\bra t^{\mathbb Z}\ket}\subset {^*\mathbb R}\langle t^{\mathbb R}\rangle\subset {^\rho\mathbb R}.
\end{align} 
We should mention that $^\rho\mathbb R$ is unique up to a field isomorphism (it does not depend on the particular choice of the ultrafilter $\mathcal U$ and the choice of the scale $\rho$) by Theorem~\ref{T: Second Uniqueness Result}.


\section{The Purge of Infinitesimals from Mathematics}\label{S: The Purge of Infinitesimals from Mathematics}

In this section we offer a short survey on the history of infinitesimal calculus written in a \emph{polemic-like style}. The purpose is to refresh the memory of the readers on one hand, and to prepare them for the next section on the other, where we shall claim \emph{the main point of our article}. For a more detailed exposition on the subject we refer to the recent article by Borovik \& Katz~\cite{BorovikKatz}, where the reader will find more references on the subject. For a historical research on the invention of infinitesimal calculus in the context of the Reformation and English Revolution we enthusiastically refer the reader to the excellent recent book by Amir Alexander~\cite{aAlexander2014}. For those readers who are interested in the philosophical roots of the infinitesimal calculus in connection with the Hegel dialectics and logical paradoxes in set theory and quantum mechanics, we refer to the work of Bulgarian philosopher Sava Petrov~\cite{sPetrovArticle}-\cite{sPetrovBook}. 

\begin{itemize}
\item The Infinitesimal calculus was founded as a mathematical discipline by Leibniz and Newton, but the origin of \emph{infinitesimals} can be traced back to Galileo, Cavalieri, Torricelli, Fermat, Pascal and even to Archimedes. The development of calculus culminated in Euler's mathematical inventions. Perhaps Cauchy was the last -- among the great mathematicians -- who still taught calculus (in \'{E}cole) and did research in terms of infinitesimals. We shall refer to this period of analysis as the \emph{Leibniz-Euler Infinitesimal Calculus} for short. 

\item There has hardly ever been a more fruitful and exciting period in mathematics than during the time the Leibniz-Euler infinitesimal calculus was developed. New important results were pouring down from every area of science to which the new method of infinitesimals had been applied -- integration theory, ordinary and partial differential equations, geometry, harmonic analysis, special functions, mechanics, astronomy and physics in general. The mathematicians were highly respected in the science community for having ``in their pockets'' a new powerful method for analyzing everything ``which is changing.'' We might safely characterize the  \emph{Leibniz-Euler Infinitesimal Calculus} as the ``golden age of mathematics.'' We should note that all  of the mathematical achievements of infinitesimal calculus have survived up to modern times. Furthermore, our personal opinion is that the infinitesimal calculus has never encountered logical paradoxes -- such as Russell's paradox in set theory, for example.

\item Regardless of the brilliant success and the lack of (detected) logical paradoxes, doubts about the philosophical and mathematical legitimacy of the foundation of infinitesimal calculus started from the very beginning. The main reason for worry was one of the principles (axioms) -- sometimes called the Leibniz principle -- which claims that there exists a non-Archimedean totally ordered field with very special properties (a non-standard extension of an Archimedean field -- in modern terminology). This principle is not intuitively believable, especially if compared with the axioms of Euclidean geometry. After all, it is much easier to imagine ``points, lines and planes'' around us, rather than to believe that such things like an ``infinitesimal amount of wine'' or ``infinitesimal annual income'' might possibly have counterparts in the real world. The mathematicians of the $17^\textrm{th}$ and $18^\textrm{th}$ centuries  hardly had any experience with non-Archimedean fields -- even the simplest such field $\mathbb Q(t)$ was never seriously considered as a ``field extension'' (in modern terms) of $\mathbb Q$. 

\item About the war waged by the \emph{Jesuit Order} (known also as the \emph{Society of Jesus}) against the infinitesimals and mathematicians who dared to use them in the context of the Reformation and Counter-Reformation, we refer the reader to the recent book by Amir Alexander~\cite{aAlexander2014}.

\item  Looking back with the eyes of a modern mathematician endowed with Robinson's non-standard analysis (Robinson~\cite{aRob66}), we can now see that the Leibniz-Euler calculus was actually quite rigorous -- at least much more rigorous than perceived by many modern mathematicians today and certainly by Weierstrass, Bolzano and Dedekind, who started the \emph{reformation of calculus} in the second part of the $19^\textrm{th}$ century. All axioms (or principles) of the infinitesimal calculus were correctly chosen and eventually survived the test of the modern non-standard analysis invented by A. Robinson in the 1960's. What was missing at the beginning of the $19^\textrm{th}$ century to complete this theory was a proof of the consistency of its axioms; such a proof requires -- from a modern point of view -- only two more things: Zorn's lemma (or equivalently, the axiom of choice) and a construction of a complete totally ordered field from the rationals. 

\item Weierstrass, Bolzano and Dedekind, along with many others, started the \emph{reformation of calculus} by expelling the infinitesimals and replacing them by the concept of the \emph{limit}. Of course, the newly created \emph{real analysis} also requires Zorn's lemma, or the equivalent axiom of choice, but the $19^\textrm{th}$ century mathematicians did not worry about such ``minor details,'' because most of them (with the possible exception of Zermelo) perhaps did not realize that \emph{real analysis} cannot possibly survive without the axiom of choice. The status of Zorn's lemma and the  axiom of choice were clarified a hundred years later by P. Cohen, K. G\"{o}del and others. Dedekind however (along with many others) constructed an example of a complete field, later called the \emph{field of Dedekind cuts}, and thus proved the consistency of the axioms of the real numbers. This was an important step ahead which was missing in the infinitesimal calculus.

	\item The \emph{purge of the infinitesimals} from calculus and from mathematics in general however came at a very high price (paid nowadays by the modern students in real analysis): the number of quantifiers in the definitions and theorems in the new \emph{real analysis} was increased by at least two additional quantifiers when compared to their counterparts in the \emph{infinitesimal calculus}. For example, the definition of a \emph{limit} or \emph{derivative} of a function in the Leibniz-Euler infinitesimal calculus requires only one quantifier (see Theorem~\ref{T: Limit} and Theorem~\ref{T: Derivative}). In contrast, there are three non-commuting quantifiers in their counterparts in real analysis. In the middle of the $19^\textrm{th}$ century however, the word ``infinitesimals'' had become synonymous to ``non-rigorous'' and the mathematicians were ready to pay about any price to get rid of them. 

\item Starting from the beginning of the $20^\textrm{th}$ century \emph{infinitesimals} were systematically expelled from mathematics -- both from textbooks and research papers. The name of the whole discipline \emph{infinitesimal calculus} became archaic and was first modified to \emph{differential calculus}, and later to simply \emph{calculus}, perhaps in an attempt to erase even the slightest remanence of the \emph{realm of infinitesimals}. Even in the historical remarks spread in the modern real analysis textbooks, the authors often indulge in a sort of rewriting of the history by discussing the history of infinitesimal calculus, but not even mentioning the word ``infinitesimal.'' After almost 300 year Jesuit Order's dream -- to expel the infinitesimals from mathematics (Alexander~\cite{aAlexander2014}) -- was finally completely and totally realized: A contemporary student in mathematics might very well graduate from college without ever hearing anything about infinitesimals. Even professional mathematicians (Fields medalists are not excluded)  might have troubles in presenting a simple example of a \emph{field with infinitesimals} (although everyone knows that ''Leibniz used infinitesimals'' and that ``Robinson invented the non-standard analysis'').

\item The \emph{differentials} were also not spared from the purge -- because of their historical connection with infinitesimals. Eventually they were ``saved'' by the differential geometers under a new name: the \emph{total differentials} from infinitesimal calculus were renamed in  modern geometry to \emph{derivatives}. The sociologists of science might take note: it is not unusual in \emph{politics} or other more ideological fields to ``save'' a concept or idea by simply ``renaming it,'' but in mathematics this happens very, very rarely. The last standing reminders of the ``once proud infinitesimals'' in the modern mathematics are perhaps the ``symbols'' $dx$ and $dy$ in the Leibniz notation $dy/dx$ for derivative and in the integral $\int f(x)\, dx$, whose resilience  turned out to be without precedent in mathematics. An innocent and confused student in a modern calculus course, however, might ponder for hours over the question what the deep meaning (if any) of the word ``symbol" is. For a point of view -- somewhat different from ours -- about whether and to what extend the infinitesimals survives the ``purge", we refer the reader to Ehrlich~\cite{pEhrlich}.

\item In the 1960's,  A. Robinson invented non-standard analysis and Leibniz-Euler infinitesimal calculus was completely and totally rehabilitated. The attacks against the infinitesimals finally ceased, but the straightforward hatred toward them remains -- although rarely  expressed openly anymore. (We have reason to believe that the second most hated notion in mathematics after ``infinitesimals'' is perhaps ``asymptotic series,'' but this is a story for another time.) In the minds of many, however, there still remains the lingering suspicion that non-standard analysis is a sort of ``trickery of overly educated logicians'' who -- for lack of anything else to do -- ``only muddy the otherwise crystal-clear waters of modern real analysis.'' 

\item Summarizing the above historical remarks,  our overall impression is -- said figuratively -- that most modern mathematicians perhaps feel much more grateful to Weierstrass, Bolzano and Dedekind, than to Cavalieri, Torricelli, Pascal, Fermat, Leibniz, Newton, L'Hopital and Euler. And many of them perhaps would be happier now if the non-standard analysis had never been invented.
\end{itemize}

\section{How Rigorous Was the Leibniz-Euler Calculus}\label{S: How Rigorous Was the Leibniz-Euler Calculus}


 The Leibniz-Euler infinitesimal calculus was based on the existence of two totally ordered fields -- let us denote them by $\mathbb L$ and $^*\mathbb L$. We shall call $\mathbb L$ the \emph{Leibniz field} and $^*\mathbb L$ its \emph{Leibniz extension}. The identification of these fields has been a question of debate up to present times. What is known with certainty is the following: (a) $\mathbb L$ is an Archimedean field and $^*\mathbb L$ is a non-Archimedean field (in the modern terminology); (b)  ${^*\mathbb L}$ is a proper order field extension of $\mathbb L$; (c) $\mathbb L$ is Leibniz complete (see Axiom 1 below); (d) $\mathbb L$ and $^*\mathbb L$ satisfy the \emph{Leibniz Transfer Principle} (Axiom 2 below). 

\begin{remark}[About the Notation] The set-notation we just used to describe the infinitesimal calculus -- such as $\mathbb L, {^*\mathbb L}$, as well as $\mathbb N, \mathbb Q, \mathbb R$, etc. -- were never used in the $18^\textrm{th}$ century, nor for most of the $19^\textrm{th}$ century. Instead, the elements of $\mathbb L$ were described verbally as the ``usual quantities'' in contrast to the elements of $^*\mathbb L$  which were described in terms of infinitesimals: $dx, dy, 5+dx$, etc.. In spite of that, we shall continue to use the usual set-notation to facilitate the discussion. 
\end{remark}

	One of the purposes of this article is to try to convince the reader that the above assumptions for $\mathbb L$ and $^*\mathbb L$ imply that $\mathbb L$ is a complete field and thus isomorphic to the field of reals, $\mathbb R$. That means that the Leibniz-Euler infinitesimal calculus was already a rigorous branch of mathematics -- at least much more rigorous than many contemporary mathematicians prefer to believe. Our conclusion is that the amazing success of the infinitesimal calculus in science was possible, we argue, \textbf{not in spite of lack of rigor, but because of the high mathematical rigor} already embedded in the formalism. 

	All of this is in sharp contrast to the prevailing perception among many contemporary mathematicians that the Leibniz-Euler infinitesimal calculus was a non-rigorous branch of mathematics. Perhaps, this perception is due to the wrong impression which most modern calculus textbooks create. Here are several popular myths about the level of mathematical rigor of the infinitesimal calculus. 

\begin{myth} 
   Leibniz-Euler calculus was non-rigorous because it was based  on the concept of \emph{non-zero infinitesimals}, rather than on \emph{limits}. The concept of \emph{non-zero infinitesimal} is perhaps ``appealing for the intuition,'' but it is certainly mathematically non-rigorous. ``There is no such thing as a non-zero infinitesimal.'' The \emph{infinitesimals} should be expelled from mathematics once and for all, or perhaps, left only to the applied mathematicians and physicists to facilitate their intuition.
\end{myth}

\begin{fact}
   Yes, the Archimedean fields do not contain non-zero infinitesimals. In particular, $\mathbb R$ does not have non-zero infinitesimals. But in mathematics there are also non-Archimedean ordered fields and each such field contains infinitely many non-zero infinitesimals.  The simplest example of a non-Archimedean field is, perhaps, the field $\mathbb R(t)$ of rational functions with real coefficients supplied with ordering as in Example~\ref{Ex: Field of Rational Functions} in this article. Actually, every totally ordered field which contains a proper copy of $\mathbb R$ is non-Archimedean (see Section~\ref{S: Infinitesimals in Algebra and Non-Standard Analysis}). Blaming the \emph{non-zero infinitesimals} for the lack of rigor is \emph{nothing other than mathematical ignorance}! 
\end{fact}

\begin{myth}
   The Leibniz-Euler infinitesimal calculus was non-rigorous because of the lack of the completeness of the field of ``ordinary scalars'' $\mathbb L$.  Perhaps $\mathbb L$ should be identified with the field of rationals $\mathbb Q$, or the field $\mathbb A$ of the real algebraic numbers? Those who believe that the  Leibniz-Euler infinitesimal calculus was based on a non-complete field -- such as $\mathbb Q$ or $\mathbb A$ -- must face a very confusing mathematical and philosophical question: How, for God's sake, such a non-rigorous and naive framework as the field of rational numbers $\mathbb Q$ could support one of the most successful developments in the history of mathematics and science in general? Perhaps mathematical rigor is irrelevant to the success of mathematics? Even worse: perhaps mathematical rigor should be treated as an ``obstacle'' or ``barrier'' in the way of the success of science. This point of view is actually pretty common among applied mathematicians and theoretical physicists. We can only hope that those who teach real analysis courses nowadays do not advocate these values in class.
\end{myth}

\begin{fact}
   The answer to the question ``was the Leibniz field $\mathbb L$ complete'' depends on whether or not the Leibniz extension $^*\mathbb L$ can be viewed as a ``non-standard extension'' of $\mathbb L$ in the sense of the modern non-standard analysis. Why? Because the result in Theorem~\ref{T: Completeness of an Archimedean Field} of this article shows that if the Leibniz extension $^*\mathbb L$ of $\mathbb L$ is in fact a non-standard extension of $\mathbb L$, then $\mathbb L$ is a  complete Archimedean field which is thus isomorphic to the field of real numbers $\mathbb R$. On the other hand, there is plenty of evidence that Leibniz and Euler, along with many other mathematicians, had regularly employed the following principle:

   \begin{axiom}[Leibniz Completeness Principle]
      Every finite number in $^*\mathbb L$ is infinitely close to some (necessarily unique) number in $\mathbb L$ (\#2 of Definition~\ref{D: Completeness of a Totally Ordered Field}).
   \end{axiom}
\end{fact}

\begin{remark} The above property of $^*\mathbb L$ was treated by Leibniz and the others as an ``obvious truth.'' More likely, the $18^\textrm{th}$ century mathematicians were unable to imagine a counter-example to the above statement. The results of non-standard analysis produce such a counter-example: there exist finite numbers in $^*\mathbb Q$ which are \emph{not} infinitely close to any number in $\mathbb Q$.
\end{remark}

\begin{myth}
   The theory of non-standard analysis is an invention of the $20^\textrm{th}$ century and has nothing to do with the Leibniz-Euler infinitesimal calculus. We should not try to rewrite the history and project backwards the achievements of modern mathematics. The proponents of this point of view also emphasize the following features of non-standard analysis:
   \begin{R-enum}
   \item A. Robinson's original version of non-standard analysis was based of the so-called \emph{Compactness Theorem} from model theory: If a set $S$ of sentences has the property that every finite subset of $S$ is consistent (has a model), then the whole set $S$ is consistent (has a model). 

   \item The ultrapower construction of the non-standard extension $^*\mathbb K$ of a field $\mathbb K$ used in Example 5, Section \ref{S: Infinitesimals in Algebra and Non-Standard Analysis}, is based on the existence of a free ultrafilter. Nowadays we prove the existence of such a filter with the help of Zorn's lemma.  Actually the statement that \emph{for every infinite set $I$ there exists a free ultrafilter on $I$} is known in modern set theory  as the \emph{free filter axiom} (an axiom which is weaker than the axiom of choice).
   \end{R-enum} 
\end{myth}

\begin{fact}
   We completely and totally agree with both (1) and (2) above. Neither the \emph{completeness theorem} from model theory, nor the \emph{free filter axiom} can be recognized  in any shape or form in the Leibniz-Euler infinitesimal calculus.  These inventions belong to the late $19^\textrm{th}$ and the first half of $20^\textrm{th}$ century. Perhaps surprisingly for many of us, however, J. Keisler~\cite{jKeislerF} invented a simplified version of non-standard analysis -- general enough to support calculus -- which rely on neither model theory or formal mathematical logic. It presents the definition of $^*\mathbb R$ axiomatically in terms of a particular extension of all functions from $\mathbb L$ to $^*\mathbb L$ satisfying the so-called \emph{Leibniz Transfer Principle}:

   \begin{axiom}[Leibniz Transfer Principle]\label{A: Leibniz Transfer Principle} 
      For every $d\in\mathbb N$ and for every set $S\subset\mathbb L^d$ there exists a unique set $^*S\subset{^*\mathbb L^d}$ such that:
      \begin{R-enum}
      \item $^*S \cap \mathbb L^d=S$.
      \item If $f\subset \mathbb L^p\times \mathbb L^q$ is a function, then $^*f\subset{^*\mathbb L^p}\times{^*\mathbb L^q}$ is also a function. 
      \item $\mathbb L$ satisfies Theorem~\ref{T: Keisler Transfer Principle} for $\mathbb K=\mathbb L$. 
      \end{R-enum}
   \end{axiom}

   We shall call $^*S$ a \emph{non-standard extension} of $S$ borrowing the terminology from Example 5, Section~\ref{S: Infinitesimals in Algebra and Non-Standard Analysis}. 
\end{fact}

\begin{examples} Here are two (typical) examples for the application of the Leibniz transfer principle:
   \begin{Ex-enum}
\item $(x+y)^3=x^3+3x^2y+3xy^2+y^3$ holds for all $x, y\in{\mathbb L}$ if and only if this  identity holds for all $x, y\in{^*\mathbb L}$.
   \item The identity $\sin(x+y)={\sin x}\, {\cos y}+{\cos x}\, {\sin y}$ holds for all $x, y\in{\mathbb L}$ if and only if this  identity holds for all $x, y\in{^*\mathbb L}$ (where the asterisks in front of the sine and cosine are skipped for simplicity). 
   \end{Ex-enum}
\end{examples} 

 Leibniz never formulated his principle exactly in the form presented above. For one thing, the set-notation such as $\mathbb N$, $\mathbb Q$, $\mathbb R$, $\mathbb L$, etc. was not in use in the $18^\textrm{th}$ century. The name ``Leibniz Principle'' is often used in the modern literature (see Keisler~\cite{jKeislerF}, p. 42 or Stroyan \& Luxemburg~\cite{StroyanLux76}, p. 28), because Leibniz suggested that the field of the usual numbers ($\mathbb L$ or $\mathbb R$ here) should be extended to a larger system of numbers ($^*\mathbb L$ or $^*\mathbb R$), which has the \emph{same properties, but contains infinitesimals}. Both Axiom 1 and Axiom 2 however, were in active use in Leibniz-Euler infinitesimal calculus.  Their implementation does not require an elaborate set theory or formal logic; \emph{what is a solution of a system of equations and inequalities} was perfectly clear to mathematicians long before of the times of Leibniz and Euler. Both Axiom 1 and Axiom 2 are theorems in modern non-standard analysis (Keisler~\cite{jKeislerF}, p. 42). However, if Axiom 1 and Axiom 2 are understood as \emph{axioms}, they characterize the field $\mathbb L$ uniquely (up to a field isomorphism) as a complete Archimedean field (thus a field isomorphic to $\mathbb R$). Also, these axioms characterize $^*\mathbb L$ as a \emph{non-standard extension} of $\mathbb L$. True, these two axioms do not determine $^*\mathbb L$ uniquely (up to a field isomorphism) unless we borrow from the modern set theory such tools as \emph{cardinality} and the \emph{GCH}, but for the rigorousness of the infinitesimal this does not matter. Here is an example how the formula $(x^3)^\prime= 3x^2$ was derived in the infinitesimal calculus: suppose that $x\in \mathbb L$. Then for every non-zero infinitesimal $dx\in{^*\mathbb L}$ we have 
\begin{align}
&\frac{(x+dx)^3-x^3}{dx}= \frac{x^3+3x^2\, dx+3x\, dx^2+dx^3-x^3}{dx}=\notag\\
&=\frac{(3x^2+3x\, dx+dx^2)\, dx}{dx}=3x^2+3x\, dx+dx^2\approx 3x^2,\notag
\end{align}
because $3x\, dx+dx^2\approx 0$. Here $\approx$ stands for the infinitesimal relation on $^*\mathbb L$, i.e. $x\approx y$ if $x-y$ is infinitesimal (Definition~\ref{D: Infinitesimals, etc.}). Thus $(x^3)^\prime= 3x^2$ by the Leibniz definition of derivative (Theorem~\ref{T: Derivative}). For those who are interested in teaching calculus through infinitesimals we refer to the calculus textbook Keisler~\cite{jKeislerE} and its more advanced companion Keisler~\cite{jKeislerF} (both available on internet). On a method of teaching limits through infinitesimals we refer to Todorov~\cite{tdTod2000a}.

\begin{myth}
   Trigonometry and the theory of algebraic and transcendental elementary functions such as $\sin x, e^x$, etc. was not rigorous in the infinitesimal calculus. After all, the theory of analytic functions was not developed until late in $19^\textrm{th}$ century.   
\end{myth}

\begin{fact}
   Again, we argue that the rigor of trigonometry and the elementary functions was relatively high and certainly much higher than in most of the contemporary trigonometry and calculus textbooks. In particular, $y=\sin x$ was defined by first, defining $\sin^{-1} y=\int_0^x\frac{dy}{\sqrt{1-y^2}}$ on $[-1, 1]$ and geometrically viewed as a particular \emph{arc-length on a circle}. Then $\sin x$ on $[-\pi/2, \pi/2]$ is defined as the inverse of $\sin^{-1} y$. If needed, the result can be extended to $\mathbb L$ (or to $\mathbb R$) by periodicity. This answer leads to another question: how was the \emph{concept of arc-length} and the integral $\int_a^b f(x)\, dx$ defined in terms of infinitesimals before the advent of Riemann's theory of integration? On this topic we refer the curious reader to Cavalcante \& Todorov~\cite{CavTod08}.
\end{fact}


\begin{thebibliography}{9}

\bibitem{aAlexander2014} Amir Alexander, \emph{Infinitesimals: How a Dangerous Mathematical Theory shaped the Modern Would}, Scientific American/Farrar, Straus and Giroux, New York, First Edition, 2014.
\bibitem{ArtinSchreier27}E. Artin and E. Schreier, {\em Algebraische Konstruction reeller K\"{o}rper}, Abh. Math. Sem. Hansischen Univ. 5 (1927) pp. 85-99.

\bibitem{bana} B. Banaschewski. \emph{On Proving the Existence of Complete Ordered Fields.} American Math Monthly 105(6), pp. 548-551.
\bibitem{bartle} R. G. Bartle and D. R. Sherbert. \emph{Introduction to Real Analysis}. Wiley, third edition, 1999.
\bibitem{Katz at al 2014} T. Bascelli, E. Bottazzi, F. Herzberg, V. Kanovei, K.U. Katz, M.G. Katz, T. Nowik, D. Sherry and St. Shnider, \emph{Fermat, Leibniz, Euler, and the Gang: The True History of the Concepts of Limit and Shadow}, Notices of the MAS, Volume 61, Number 8, September, 2014.

  

\bibitem{BorovikKatz} A. Borovik and M.G. Katz, \emph{Who gave you the Cauchy-Weierstrass Tale? The Dual History of Rigorous Calculus} to appear in Foundations of Science.

\bibitem{CapinskiCutland95} M. Capi\'{n}ski and N. J. Cutland, Nonstandard Methods for Stochastic Fluid Mechanics, World Scientific, Singapore-New Jersey-London-Hong Kong, 1995.

\bibitem{CavTod08} Ray Cavalcante and Todor D. Todorov, \emph{A Lost Theorem: Definite Integrals In Asymptotic Setting}, The American Mathematical Monthly, Volume 115, Number 1, January, 2008, pp. 45-56 (available at ArxivMathematics: [http://arxiv.org/abs/0804.3156v1]).

\bibitem{cavalcante} R. Cavalcante. \emph{Reduction of the Number of Quantifiers in Real Analysis through Infinitesimals}, 2008. arXiv:0809.4814v2.

\bibitem{cyChristov74}  Chr. Ya. Christov, \emph{Eine neue Art von verallgemeinerten Funktionen}.-Nova Acta Leopoldina. Neue Folge, 212, Band 39, 1974, 181-1944. 

\bibitem{ChrTod84}  Chr. Ya. Christov, T. D. Todorov, {\em Asymptotic Numbers: Algebraic 	Operations with Them}, In Serdica, Bulgaricae
Mathematicae  Publicationes, Vol.2, 1974, p.~87--102. 



\bibitem{davis} M. Davis, \emph{Applied Non-standard Analysis}. Dover, 2005.

\bibitem{pEhrlich} Philip Ehrlich, {\em The Rise of non-Archimedean Mathematics and the Roots of a Misconceptions I: The Emergence of non-Archimedean Systems of Magnitudes}, Arch. Hist. Exact Sci. 60 (2006) 1121 
(Digital Object Identier (DOI) 10.1007/s00407-005-0102-4).

\bibitem{ErdGillHenr55} P. Erd\"{o}s, L. Gillman and M. Henriksen, {\em An Isomorphism Theorem for Real-Closed Fields}, Annals of
Mathematics, Vol. 61, No. 3, May 1955, p.~542--560.

\bibitem{DalWoodin} H. Garth Dales and W. Hugh Woodin, {\em Super-Real Fields: Totally Ordered Fields with Additional Structure}, Oxford Science Publications, London Mathematical Monographs-New Series {\bf 14}, Clarendon Press, Oxford, 1996.

\bibitem{lFux63} L. Gillman and M. Jerison, {\em Rings of Continuous Functions}, Springer-Verlag, New York, Berlin, Heidelberg, London, Paris, Tokyo, Hong Kong, Barcelona, Budapest, 1976.

\bibitem{fqGouv} Fernando Q. Gouv, {\em $p$-Adic Numbers. An Introduction}, Springer, 1997.

\bibitem{hHahn} H. Hahn, {\em \"{U}ber die nichtarchimedischen Gr\"{o}ssensysteme}, Sitz. K. Akad. Wiss. {\bf 116} (1907), p.~601-655.
\bibitem{tHungerford} Thomas W. Hungerford, \emph{Algebra}, Graduate Texts in Mathematics 73 (1974), Springer-New York-Berlin-Heidelberg-London-Paris-Tokyo.

\bibitem{jHall11} James Hall, \emph{Completeness of Ordered Fields (2011)}, in ArxivMathematics: (http://digitalcommons.calpoly.edu/mathsp/3/).

\bibitem{HallTodDedekind11} James F. Hall and Todor D. Todorov, \emph{Another Proof of the Existence a Dedekind Complete Totally Ordered Field (2011)}, in ArxivMathematics: (http://arxiv.org/abs/1101.3825v1).

\bibitem{hewitt} E. Hewitt and K. Stromberg. \emph{Real and Abstract Analysis}. Springer, first edition, 1965.

\bibitem{hilbert} D. Hilbert, \" Uber den Zahlbegriff, \emph{Jber. Deutsche Math. Verein.} 8 (1900).

\bibitem{tHungerford} Thomas W. Hungerford, \emph{Algebra}, Graduate Texts in Mathematics 73 (1974), Springer-New York-Berlin-Heidelberg-London-Paris-Tokyo.

\bibitem{jKeislerE} H. J. Keisler, \emph{Elementary Calculus: An Approach Using Infinitesimals},  Prindle, Weber \& Schmidt, Boston, 1976 (http://www.math.wisc.edu/\newline~keisler/calc.html).

\bibitem{jKeislerF} H. J. Keisler, \emph{Foundations of Infinitesimal Calculus}, Prindle, Weber~\&~Schmidt, 
Boston 1976 (http://www.math.wisc.edu/~keisler/\newline foundations.html). 

\bibitem{KeislerSchmerl91} H. Jerome Keisler and James Schmerl,
\emph{Making the hyperreal line both saturated and complete},
Journal of Symbolic Logic 56 (1991), pp. 1016-1025.

\bibitem{jKelley} J. L. Kelley,  \emph{General Topology}, Prindle, Springer-Verlag, New York, Berlin, Heidelberg,  Tokyo, 1975.

\bibitem{krull} W. Krull, \emph{Allgemeine Bewertungstheorie}, Journal f\"{u}r die reine und angewandte Mathematik 167 (1932), p. 225-236.
\bibitem{lang} S. Lang, Algebra, Addison-Wesley, 1992.
\bibitem{Laugwitz} D. Laugwitz. \emph{Eine Nichtarchimedische Erweiterung Angeordneter K\"orper}, Math. Nachrichte 37 (1968), p. 225-236.

\bibitem{LC} T. Levi-Civit{\'a}, \emph{Sugli Infiniti ed Infinitesimi Attuali Quali Elementi Analitici} (1892-1893), Opere Mathematiche, vol. 1, Bologna (1954), p.~1--39.

\bibitem{LiRob} A. H. Lightstone and A. Robinson, \emph{Nonarchimedean Fields and Asymptotic Expansions}, North-Holland-Amsterdam-New York-Oxford, Vol. 13, 1975. 

\bibitem{lindstrom} T. Lindstr\o m, An invitation to nonstandard analysis. In: Cutland N (ed) \emph{Nonstandard Analysis and its applications}. Cambridge University Press, London, 1988, pp 1-105.



\bibitem{wLux76} W. A. J. Luxemburg, \emph{On a class of valuation fields introduced by A. Robinson}, Israel J. Math. \textbf{25} (1976), p.~189--201.

\bibitem{OberTod98} M. Oberguggenberger and T. Todorov, {\em An Embedding of  Schwartz Distributions in the Algebra of Asymptotic Functions}, In: \emph{International Journal of Mathematics} \&  \emph{Mathematical Sciences}, Vol. 21, No. 3 (1998), p.~417--428. 

\bibitem{oconnor} J. J. O'Connor and E. F. Robertson, \emph{History topic: The real numbers: Stevin to Hilbert}, October 2005. \url{http://www-history.mcs.st-and.ac.uk/PrintHT/Real_numbers_2.html}

\bibitem{aOstrowski} A. Ostrowski, \emph{Untersuchungen zur arithmetischen Theorie der K\"{o}rper}, Math. Z., 39 (1935), 269-404.

\bibitem{vPestov} G. G. Pestov, \emph{Structure of Ordered Fields}, Toms University Press, 	Tomsk, 1980 (in Russian).

\bibitem{sPetrovArticle} Sava Petrov, \emph{Infinitesimal Paradoxes}, Acad\'{e}mie Bulgare des Sciences, Bulletin de L'Institut de Philosophie, XX, 1971 (In Bulgarian language with one page long summary in English).

\bibitem{sPetrovBook} Sava Petrov, \emph{Logical Paradoxes in Philosophical Interpretation}, Nauka i Izkustvo, Sofia, 1971 (In Bulgarian language with a 24-pages long summary in English).


\bibitem{aPrestel} A. Prestel. \emph{Lectures on formally real fields, Lecture notes in Mathematics 1093}, Springer, New York, 1984.

\bibitem{jPropp} James Propp, \emph{Real Analysis in Reverse}, in (http://faculty.uml.edu/\newline jpropp/reverse.pdf).

\bibitem{riben} P. Ribenboim, \emph{The Theory of Classical Valuation}, Springer Monographs in Mathematics, Springer-Verlag, 1999.

\bibitem{aRob66} A. Robinson, {\em Nonstandard Analysis}, North Holland, Amsterdam, 1966.



\bibitem{aRob73} A. Robinson, \emph{Function theory on some nonarchimedean fields}, Amer. Math. Monthly 80 (6),
Part~II: Papers in the Foundations of Mathematics (1973), p.~87--109.

\bibitem{poma} W. Rudin. \emph{Principles of Mathematical Analysis}. McGraw Hill, third edition, 1976.

\bibitem{StroyanLux76} K. D. Stroyan and W. A. J. Luxemburg, \emph{Introduction to the Theory of Infinitesimals}, Academic Press, New York, 1976.

\bibitem{hTeismann2013} Holger Teismann, \emph{ Toward a More Complete List of Completeness Axioms}, The American Mathematical Monthly, February 2013, p. 99-114.

\bibitem{tdTod81}  T.D. Todorov, {\em Asymptotic Functions and the Problem of Multiplication of Schwartz Distributions}, In: \emph{Bulgarian Journal of Physics},
Vol. 8 (1981), 2, p.~109--120. 

\bibitem{tdTod2000a} Todor~D. Todorov, \emph{Back to Classics: Teaching Limits through Infinitesimals}, International Journal of Mathematical Education in Science and Technology, 2001, vol. 32, no. 1, p. 1-20 (available at ArxivMathematics: [http://arxiv.org/abs/1108.4657]).

\bibitem{TodVern08} Todor Todorov and Hans Vernaeve, \emph{Full Algebra of Generalzed Functions and Non-Standard  Asymptotic Analysis}, in Logic and Analysis, Springer, Vol. 1, Issue 3, 2008, pp. 205-234 (available at ArxivMathematics: [http://arxiv.org/abs/0712.2603]).

\bibitem{TodWolf04} T. Todorov and R. Wolf, \emph{Hahn field representation of A. Robinsons asymptotic numbers}, in  Nonlinear Algebraic Analysis and Applications, Proceedings of the International Conference on Generalized Functions (ICGF) 2000, Edited by A. Delcroix, M. Hasler, J.-A. Marti, and V.Valmorin, Cambridge Scientific Publishers, Cottenham, Cambridge, 2004, pp. 357-374 (available at ArxivMathematics: [http://arxiv.org/abs/math/0601722]).

\bibitem{tdTodAxioms10} Todor D. Todorov, {\em An axiomatic approach to the non-linear theory of generalized functions and consistency of Laplace transforms}, In: \emph{Integral Transforms and Special Functions}, Volume 22, Issue 9, September 2011, p. 695-708 (available at arXivMathematics: (http://arxiv.org/abs/1101.5740)).

\bibitem{tdTodAlgebraic13} Todor D. Todorov, {\em Algebraic Approach to Colombeau Theory}, In: \emph{San Paulo Journal of Mathematical Sciences}, \textbf{7} (2013), no. 2, 127-142 (http://arxiv.org/abs/1405.7341).

\bibitem{tdTodLightenings15} Todor D. Todorov, \emph{Steady-State Solutions in an Algebra of Generalized Functions: \small{Lightning, Lightning Rods and Superconductivity}}, to appear.

\bibitem{VanDerWaerden} B. L. van der Waerden. \emph{Algebra}. Springer, seventh edition, 1966.
\end{thebibliography}






\end{document}








