/* Off-Script Rich — the one list of guides.

   Both the library (/guides/) and the keyword router (/go/) read this file.
   Adding a guide = one object here. Nothing else to touch.

   keyword  what they comment. uppercase, letters and numbers only.
   aliases  optional. old or alternate words that should open the same guide
            (e.g. a caption that still says the old keyword).
   pillar   money | ai | life
   live     false hides it everywhere (roadmap entries).
   href     file name inside /guides/.
*/
window.OSR_GUIDES = [
    {
      keyword: "STOCKS", pillar: "money", live: true, href: "stocks.html",
      title: "the insider tape",
      desc: "every stock purchase filed by a company insider or a member of congress last week, pulled from sec and stock act filings. rebuilds itself every monday."
    },
    {
    keyword: "SHOTS", pillar: "ai", live: true, href: "shots.html",
    title: "six prompts for linkedin headshots",
    desc: "the six prompts from the reel in full, colour palettes included. swap one bracket for yourself and paste into any image tool. no photographer, no app subscription."
  },
    {
      keyword: "NUMBER", pillar: "money", live: false, href: "#",
      title: "your freedom number",
      desc: "your city, your burn, your savings rate. out comes the portfolio that covers your life permanently and how many years away it actually is."
    },
    {
      keyword: "EXPOSED", pillar: "ai", live: false, href: "#",
      title: "is ai coming for your job",
      desc: "your tasks sorted into going first, safe for now, and getting more valuable. scored against published research, not vibes. ends with one move."
    },
    {
      keyword: "SKILLS", pillar: "ai", live: false, href: "#",
      title: "five paid skills you can learn free",
      desc: "the skills worth real money right now, where to learn each one for nothing, and which fits what you already know."
    },
    {
      keyword: "STACK", pillar: "ai", live: false, href: "#",
      title: "build your own ai assistant",
      desc: "one evening, no code. the setup that actually knows your context instead of starting from zero every time you open it."
    },
    { keyword: "AI", aliases: ["AL"], pillar: "ai", live: true, href: "ai.html", title: "you're not behind on ai, here's the map", desc: "one free course for the concepts, one to learn how to work with AI, two free tools to open every day, and a seven-day plan at twenty minutes a day with the prompts." },
    { keyword: "CARDS", pillar: "money", live: true, href: "cards.html", title: "the best card for each category", desc: "the four cards from the reel with their current earn rates and fees checked, a calculator that runs your own spending through all four, and the one rule that makes any rewards card worth it." },
    { keyword: "CLAUDE", pillar: "ai", live: true, href: "claude.html", title: "five claude updates, one page", desc: "opus 5.5, chat and cowork merging, the small-business workflows, the projects coordinator and salesforce inside claude: what each one is, who has it, and what to do with it tomorrow." },
    { keyword: "DESIGN", pillar: "ai", live: true, href: "design.html", title: "five sites that make ai websites look expensive", desc: "the five design galleries from the reel, one per section of a page, plus the prompt that turns a screenshot from each into a section in your own brand." },
    { keyword: "GIT", pillar: "ai", live: true, href: "git.html", title: "fifty github tricks", desc: "the four url swaps from the reel plus 46 more: url hacks, line links, keyboard shortcuts, search filters and markdown tricks that make github faster." },
    { keyword: "GITHUB", pillar: "ai", live: true, href: "github.html", title: "ten github repos worth saving", desc: "the five repos from the reel plus the five i held back: what each one does, who it's for, and the exact line to install it. no coding background needed to read this." },
    { keyword: "HOBBIES", pillar: "life", live: true, href: "hobbies.html", title: "ten hobbies you can start this hour", desc: "the full list from the reel, ten hobbies you can start in the next hour, each with exactly what to practise in your first 20 minutes and where to learn it free." },
    { keyword: "HOBBY", pillar: "life", live: true, href: "hobby.html", title: "the five-hobby system", desc: "the five pillars from the reel as a one-page worksheet: one hobby each for your body, creativity, peace, people and growth, with how to pick, how to schedule it, and the one most people skip." },
    { keyword: "LARP", pillar: "life", live: true, href: "larp.html", title: "how to larp the person you want to be", desc: "the reel's larp idea as a practice: the character sheet, the third-person self-talk trick with research behind it, the cut list, and the daily walk script." },
    { keyword: "LAWS", pillar: "life", live: true, href: "laws.html", title: "eleven laws, and how to use each one", desc: "the eleven mental models from the reel, each with the exact version, who came up with it, how to use it this week, and where the pop version gets it wrong." },
    { keyword: "METHOD", pillar: "life", live: true, href: "method.html", title: "the theater of the mind, in four steps", desc: "the four-step identity method from psycho-cybernetics, written out as a daily 15-minute practice, with what the research actually supports and the part that's just a good story." },
    { keyword: "MINDSET", pillar: "life", live: true, href: "mindset.html", title: "everyone had a day one", desc: "a one-page practice for the gap between where you are and where you're headed: the mission card, the morning question, and the weekly receipt that keeps the day-one feeling useful instead of discouraging." },
    { keyword: "MULTIBAGGER", pillar: "money", live: true, href: "multibagger.html", title: "the nvidia paper trail", desc: "every company nvidia has a disclosed stake or investment deal in, where each one is filed, and how to track the next one yourself from sec filings before the headlines." },
    { keyword: "MUSE", pillar: "money", live: true, href: "muse.html", title: "which companies an ai agent can skip", desc: "what meta's muse agent did to travel stocks in september 2026, the twist that came the day before, and a five-question middleman test you can run on any company you own." },
    { keyword: "NETWORTH", pillar: "money", live: true, href: "networth.html", title: "five net worth habits, one page", desc: "the five things from the reel turned into a one-page setup: the three accounts, the automation, the lifestyle-creep check, the credit routine and a budget you'll actually keep, with a net worth calculator." },
    { keyword: "OODA", pillar: "life", live: true, href: "ooda.html", title: "the ooda loop, for normal decisions", desc: "the fighter-pilot decision loop from the reel as a one-page worksheet: observe, orient, decide, act, with worked examples for a text, a pitch and a purchase." },
    { keyword: "RANK", pillar: "ai", live: true, href: "rank.html", title: "the first $1,000 prompts, ranked", desc: "the three prompts and the bonus from the reel in full, plus my ranked list of the fastest ways to a first paying customer with no audience, and the prompt that ranks them for you." },
{ keyword: "VISUAL", pillar: "ai", live: true, href: "visual.html", title: "the images 2.5 prompt library", desc: "where the 1,000+ chatgpt images 2.5 prompts live, how to steal one properly, and six starter prompts for studio shoots, product campaigns, editorials and camera-roll content." },
    { keyword: "AVOID", pillar: "life", live: true, href: "avoid.html", title: "the work is not the problem", desc: "you're not avoiding the task, you're avoiding the feeling. the decoder, the ten-minute test, and the three messages you haven't sent." },
    { keyword: "BANKS", pillar: "money", live: true, href: "banks.html", title: "the account setup uneven income needs", desc: "how to run uneven creator income through four accounts — the split, the tax hold-back math, the FDIC limits, and exactly what to automate." },
    { keyword: "BOOMER", pillar: "ai", live: true, href: "boomer.html", title: "buy the business, bring the ai", desc: "the roadmap for buying a small business as its owner retires and using AI to run it better — real multiples, real SBA terms, and what to automate first." },
    { keyword: "BUILD", pillar: "ai", live: true, href: "build.html", title: "steal the craft, not the content", desc: "the exact setup, the capture step everyone skips, and the prompts that make Claude Code check its own work against the original." },
    { keyword: "DEAL", pillar: "money", live: true, href: "deal.html", title: "score the deal before you answer", desc: "a 100-point scorecard for brand deals — rate, usage, exclusivity, fit, payment terms and creative control — with a hard cut-off and five auto-fails." },
    { keyword: "ENERGY", pillar: "money", live: true, href: "energy.html", title: "the power constraint, in filings", desc: "why power is the physical limit on AI datacentres, what the announced nuclear deals actually buy, and the exact dates and filings to watch." },
    { keyword: "ENOUGH", pillar: "life", live: true, href: "enough.html", title: "hold both or lose both", desc: "how to run gratitude and ambition at the same time without one eating the other — two exercises, a weekly ledger, and a five-question check." },
    { keyword: "ETF", pillar: "money", live: true, href: "etf.html", title: "the boring method, with numbers", desc: "the boring method most retail investors skip, with the real SPIVA and SEC numbers on what picking and paying cost you over twenty years." },
    { keyword: "EVIL", pillar: "life", live: true, href: "evil.html", title: "admit it before they find it", desc: "the psychology of saying the damaging thing first: what the research actually calls it, the one variable that decides if it works, and four scripts." },
    { keyword: "FACELESS", pillar: "ai", live: true, href: "faceless.html", title: "the faceless page stack, honestly", desc: "the link to the tool from the reel, the do-it-yourself version with real prices, and the length and policy rules that decide whether it ever pays." },
    { keyword: "IDEAS", aliases: ["38"], pillar: "ai", live: true, href: "ideas.html", title: "38 places a business idea hides", desc: "the full 38-method list for finding a business idea, grouped by where the idea hides, plus the AI prompts i use to validate one before building." },
    { keyword: "MAXX", pillar: "ai", live: true, href: "maxx.html", title: "thirty days, one task a day", desc: "thirty named tasks, one a day, that take you from barely using AI to running your own agents. The full day-by-day, free." },
    { keyword: "MYSTERY", pillar: "life", live: true, href: "mystery.html", title: "how to put the mystery back", desc: "why everything feels flat once you pre-load it, plus the audit, the blackout and the questions that put the unknown back into your week." },
    { keyword: "PICKS", aliases: ["ETFS"], pillar: "money", live: true, href: "picks.html", title: "five things to check before you buy", desc: "the five-point checklist for evaluating any index fund: expense ratio, tracking difference, size and liquidity, overlap, and tax treatment." },
    { keyword: "PITCH", pillar: "money", live: true, href: "pitch.html", title: "the emails that got the yes", desc: "the four brand deal emails in full — the reply that opens negotiation, the counter, the follow-up, and the walk-away. fill in the blanks and send." },
    { keyword: "POTENTIAL", pillar: "life", live: true, href: "potential.html", title: "what to actually do with the gap", desc: "that quote probably isn't Epictetus. there are two kinds of gap, they feel different, and the fix for one makes the other worse." },
    { keyword: "RATES", aliases: ["RATE"], pillar: "money", live: true, href: "rates.html", title: "what to actually charge brands", desc: "the base rate formula, the four multipliers that move it, what 2026 benchmark data says brands really pay, and a rate card you can copy." },
    { keyword: "ROTH", pillar: "money", live: true, href: "roth.html", title: "the roth ira, in four steps", desc: "who can open one, the 2026 limits, what to do once the money is in, and the withdrawal rule nobody explains. with a calculator for your own 2026 max." },
    { keyword: "SCOREBOARD", pillar: "life", live: true, href: "scoreboard.html", title: "stop refreshing the number", desc: "what checking the balance all day actually costs you, the three-day audit that shows your real number, and the schedule that replaces it." },
    { keyword: "SLOWDOWN", pillar: "money", live: true, href: "slowdown.html", title: "how to check it yourself, monthly", desc: "the five indicators people cite for an AI bubble, what each one measures, the filing it lives in, and the honest bull and bear reading of each." },
    { keyword: "SMART", aliases: ["IQ"], pillar: "life", live: true, href: "smart.html", title: "smart people usually do know", desc: "what the research actually says about whether intelligent people know it — plus a calibration test that tells you how accurate your self-read really is." },
    { keyword: "STEPS", pillar: "money", live: true, href: "steps.html", title: "four steps, in the order that works", desc: "the four steps to financial stability in the order that actually works, the reason for that order, and a worksheet where you fill in your own numbers." },
    { keyword: "TRAVEL", pillar: "ai", live: true, href: "travel.html", title: "how to actually use all three", desc: "flight price tracking, points pricing and hotel booking in Google's AI Mode — the exact prompts, the real partner list, and where each one stops." },
    /* shoot week 4 to 10 november 2026, built 8 november */
    { keyword: "MAP", pillar: "money", live: true, href: "map.html", title: "the two-minute heatmap read", desc: "how to read the s&p 500 heatmap in two minutes every morning: what the box sizes and colours mean, the four things i look at, and the prompt that turns a screenshot into a plain-english summary." },
    { keyword: "SPACE", pillar: "money", live: true, href: "space.html", title: "how wall street counts your car from space", desc: "what alternative data is, what the berkeley satellite study actually found (4 to 5% in the three days around earnings), the oil tank and coffee examples, and what a regular investor should do with this." },
    { keyword: "HISTORY", pillar: "money", live: true, href: "history.html", title: "every midterm since 1950, one table", desc: "the s&p 500's 12-month return after all 19 midterm elections since 1950, the average, the drawdowns hiding inside the green years, and what the table can and can't tell you." },
    { keyword: "CONGRESS", pillar: "money", live: true, href: "congress.html", title: "what a flipped congress can do to your money", desc: "what democrats taking the house and senate actually changes and doesn't change for your money, when it starts, why the veto still matters, and what history says about markets after midterms." },
    { keyword: "DIP", pillar: "money", live: true, href: "dip.html", title: "dip or trap: the two-question test", desc: "the two questions i run before buying any stock that's down: is revenue still growing, and is it making more cash than it spends. where to find both numbers in five minutes, plus the prompt." },
    { keyword: "RED", pillar: "money", live: true, href: "red.html", title: "the red-day checklist", desc: "the checklist i run on a red day before i touch anything: the five questions, the wash sale rule to know before you sell at a loss, and the one thing to do at 4pm." },
    { keyword: "PAGE", pillar: "money", live: true, href: "page.html", title: "cash or finance: the one-page cheat sheet", desc: "the eight purchases from the reel sorted into cash or finance, the one rule behind all of them, the car exception explained with the rate comparison, and a blank page to sort your own list." },
    { keyword: "BUDGET", pillar: "money", live: true, href: "budget.html", title: "same la salary, two budgets", desc: "the two-column la budget from the reel, how $85k becomes about $5,300 a month after tax in california, where the $18,000 a year gap comes from, and a calculator for your own take-home." },
    { keyword: "MONTH", pillar: "money", live: true, href: "month.html", title: "the best-price calendar", desc: "the month each big purchase usually hits its best price, the eight from the reel plus the rest of the year, and how to check a deal is real before you buy." },
    { keyword: "PREP", pillar: "money", live: true, href: "prep.html", title: "the 2027 prep checklist", desc: "the three moves from the reel as a checklist: the emergency fund math for la rent with a calculator, the no-new-payments rule, and building income that doesn't depend on one employer." },
    { keyword: "FLIGHT", pillar: "money", live: true, href: "flight.html", title: "the bumped-flight script", desc: "exactly what to say at the gate if you're bumped off an oversold flight: the DOT compensation rules (200% or 400% of your one-way fare up to $1,075 or $2,150), who qualifies, and why you can turn down the voucher." },
    { keyword: "SCRIPT", pillar: "money", live: true, href: "script.html", title: "the raise plan", desc: "the plan i use for every raise: the split between living better and building, where the building half goes, and a calculator that shows what one raise turns into over ten years." },
    { keyword: "MIDDLE", pillar: "money", live: true, href: "middle.html", title: "two middleman models you can start this month", desc: "affiliate and appointment setting explained: how each one pays, how to start without a product, the FTC disclosure rule for affiliate links, and the prompts to find your first offer." },
    { keyword: "CODES", pillar: "ai", live: true, href: "codes.html", title: "chatgpt photo codes, the starter pack", desc: "the la magazine prompt from the reel plus five more photo codes for chatgpt: film strip, golden hour editorial, campaign poster, cafe candid and product flat lay. upload your photos, paste, done." },
    { keyword: "MAPS", pillar: "ai", live: true, href: "maps.html", title: "google maps + claude, the walkthrough", desc: "the four-step google maps and claude walkthrough from the reel: find local businesses with great reviews and no website, build a one-page preview with claude, and show it before you ask for anything. includes the exact prompt." },
    { keyword: "FIND", pillar: "ai", live: true, href: "find.html", title: "the find-anything-in-a-photo prompt", desc: "the prompt from the reel for finding a lost item in a photo with chatgpt, plus how to take the photo so it actually works, and the limits." },
    { keyword: "FOUNDER", pillar: "ai", live: true, href: "founder.html", title: "the six-critic prompt", desc: "the prompt from the reel that turns claude into six critics of your business idea, plus the follow-up that turns the scariest critique into a test you can run this week." },
    { keyword: "OUTLIER", pillar: "ai", live: true, href: "outlier.html", title: "the outlier finder", desc: "the outlier method from the reel: views divided by the creator's normal views, anything over 10x is an idea that worked on its own. the steps, a worksheet and the prompt i use." },
    { keyword: "RIGHTS", pillar: "money", live: true, href: "rights.html", title: "pricing ad rights and spark codes", desc: "what ad authorization and spark codes actually give a brand, why commission-only deals with ad rights cost you, how i price the two separately, and the reply to send." },
    { keyword: "BLAST", pillar: "money", live: true, href: "blast.html", title: "the three-question brand email check", desc: "the three questions i run on every brand collab email before i reply: is there a number, who decides if i get paid, and is it to me or to everyone. plus the reply i send instead of filling out the form." },
    { keyword: "VOICE", pillar: "ai", live: true, href: "voice.html", title: "clone your voice, dub your reels", desc: "the setup for cloning your voice in elevenlabs and dubbing a reel into spanish: what the free plan does and doesn't include, how to record the sample, and the disclosure rule. not sponsored." },
    { keyword: "SYSTEM", pillar: "ai", live: true, href: "system.html", title: "the notion content system", desc: "my one-database notion content system: the exact properties, the four views, and the notion agent prompt that plans a week of reels. works on any plan, the agent needs business. not sponsored." },
    { keyword: "SUBS", pillar: "money", live: true, href: "subs.html", title: "the subscription audit", desc: "a free 20-minute subscription audit you can do with your bank statement, your california cancellation rights, and the fine print on apps like rocket money before you hand over a cut. not sponsored." },
    { keyword: "SAFE", pillar: "money", live: true, href: "safe.html", title: "where i keep my emergency fund, and why", desc: "how fdic insurance actually works ($250,000 per depositor, per bank, per ownership category), how cash accounts like wealthfront spread money across program banks for up to $8 million of coverage, and the checks i run before i park cash anywhere. not sponsored." }
  ];
