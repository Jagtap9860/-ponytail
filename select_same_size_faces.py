# Python Script, API Version = V19
# -*- coding: utf-8 -*-
"""Select All Same-Size Faces (per body) - one file, two lives.

INSIDE SPACECLAIM / DISCOVERY:
  Run this in the Script Editor (Design tab > Script > Run) or publish it as
  a ribbon button via Publish Script Tool. A floating panel appears and STAYS
  OPEN: click faces in the model (single or several, any bodies), then press
  "Select Similar Faces". Every face with the same surface area as ANY picked
  face, on the SAME body as that face, joins the selection - e.g. two adjacent
  faces of a box select both size-pairs on that box; identical boxes elsewhere
  stay untouched. Repeat freely; close the panel when done.

OUTSIDE SPACECLAIM (`python select_same_size_faces.py`):
  Five egotists (runtime, static, adversarial, integration, minimalism) charge
  this file with bugs; only twice-reproducible charges survive. Exit 0 = clean.

ponytail: "same size" = same surface area within AREA_TOL; a same-area but
differently-shaped face on the same body also matches (upgrade: perimeter check).
"""
AREA_TOL = 1e-6  # relative; loosen to ~1e-4 for imported/converted geometry
VERSION = "v7"   # shown in the panel title - proof of WHICH file is really running

def same_size(face, other):
    return abs(face.Area - other.Area) <= AREA_TOL * max(face.Area, other.Area)

def _set_selection(context, hits):
    """Version-safe selection assignment. Hosts disagree on what the setter
    accepts: one real host demanded ICollection<DocObject> and rejected the
    typed wrapper outright ("expected ICollection[DocObject], got ...").
    Ladder: exact demanded type first, canonical wrapper second, plain list last."""
    try:
        from System.Collections.Generic import List
        try:
            bag = List[DocObject]()  # newer hosts name the base DocObject
        except NameError:
            bag = List[DocObj]()     # older hosts: DocObj
        for face in hits:
            bag.Add(face)
    except Exception:  # no .NET interop here (e.g. the council's fake world)
        bag = hits
    try:
        context.Selection = bag
    except Exception:  # host wants an ISelection wrapper instead
        context.Selection = Selection.Create(hits)  # any failure surfaces in the panel

def expand_selection(context):
    """Grow the face selection to same-size faces on the same bodies; returns a status string."""
    all_items = list(context.Selection)
    # Duck-typed face test, no strict class check: SpaceClaim wraps faces in
    # version-namespaced classes (V19, V23...) - strictness rejected valid faces.
    picked = [x for x in all_items
              if hasattr(x, 'Area') and hasattr(getattr(x, 'Parent', None), 'Faces')]
    if not picked:
        return ("Selection had %d item(s), none a face. Pick faces (not bodies/edges)." % len(all_items)
                if all_items else "Select one or more faces in the model first.")
    bodies = []
    for face in picked:  # scan each picked body once, so results never duplicate
        if all(face.Parent is not b for b in bodies):
            bodies.append(face.Parent)
    # ponytail: O(faces x picked); trivial for brep bodies - index by rounded
    # area first if this is ever pointed at huge imported models.
    hits = [f for b in bodies for f in b.Faces
            if any(same_size(f, p) for p in picked)]
    _set_selection(context, hits)
    return "Selected %d matching face(s)." % len(hits)

def _launch_panel():  # SpaceClaim only: modeless picker, survives the script's end
    # Reference WinForms first: some SpaceClaim hosts don't auto-load that
    # separate .NET assembly - importing it cold was the line-46 ImportError.
    import clr; clr.AddReference("System.Windows.Forms")
    import System.Windows.Forms as wf
    try:  # old panels run OLD code - kill them, but never let cleanup block us
        for stale in list(wf.Application.OpenForms):
            if stale.Text.startswith("Same-Size Face Selector"):
                stale.Close()
    except Exception as e:
        print("zombie cleanup skipped: %s" % e)
    panel = wf.Form()
    panel.Text, panel.TopMost = "Same-Size Face Selector " + VERSION, True
    panel.Width, panel.Height = 280, 150
    status = wf.Label()
    status.Text = "1. Click faces in the model.\n2. Press the button below."
    status.Left, status.Top, status.Width, status.Height = 10, 10, 250, 40
    button = wf.Button()
    button.Text, button.Left, button.Top, button.Width = "Select Similar Faces", 10, 55, 250
    def on_click(sender, event_args):  # the .NET delegate keeps this alive afterwards
        try:
            status.Text = expand_selection(
                GetActiveWindow().ActiveContext)  # older SpaceClaim: Window.ActiveWindow.ActiveContext
        except Exception as e:  # interactive tool: surface the error, don't die silent
            status.Text = "Error: %s" % e

    button.Click += on_click
    panel.Controls.Add(status)
    panel.Controls.Add(button)
    panel.Show()

def _in_spaceclaim():
    try:
        GetActiveWindow
        return True
    except NameError:
        return False

def _launch_safely():  # NEVER die silent: any startup failure prints its reason
    try:
        _launch_panel()
    except Exception:
        import traceback
        traceback.print_exc()

if _in_spaceclaim():
    _launch_safely()
else:
    # Council: never runs in SpaceClaim, but IronPython 2 must still PARSE the
    # whole file - no f-strings or py3-only syntax below.
    import sys, types

    class _Face(object):  # a fake API face wrapper: area plus parent body
        def __init__(self, area, body):
            self.Area, self.Parent = area, body
    class _Body(object):
        def __init__(self, areas):
            self.Faces = [_Face(a, self) for a in areas]
    class _FaceSelection(list):
        @staticmethod
        def Create(items):
            return _FaceSelection(items)
    class _Context(object):  # setter mimics the strict host: plain collections
        # ONLY - typed wrappers are rejected, like the real TypeError did.
        def __init__(self):
            self._sel = []
        @property
        def Selection(self):
            return self._sel
        @Selection.setter
        def Selection(self, value):
            if type(value) is _FaceSelection:  # exact-type mimicry of the host's TypeError
                raise TypeError("expected ICollection[DocObject], got FaceSelection")
            self._sel = value
    _CONTEXT = _Context()
    class _Win(object):
        ActiveContext = _CONTEXT
    class _Finding(object):  # one charge of guilt; must survive re-trial
        def __init__(self, who, what, prove):
            self.who, self.what, self.prove = who, what, prove

    class _Controls(list):
        def Add(self, item):
            self.append(item)
    class _Event(object):  # minimal .NET-style event for the fake button
        def __init__(self): self.handlers = []
        def __iadd__(self, fn): self.handlers.append(fn); return self
        def fire(self):
            for fn in self.handlers: fn(None, None)
    class _Control(object):  # fake WinForms control base (Form/Label/Button)
        def __init__(self):
            self.Controls, self.Click = _Controls(), _Event()
        def Show(self):
            pass

    def _run(picked):  # execute the REAL expand_selection() against a fake world
        _CONTEXT.Selection = picked
        err = msg = None
        try:
            msg = expand_selection(_CONTEXT)
        except Exception as e:  # harness: a crash is evidence, not a pass
            err = e
        return list(_CONTEXT.Selection), err, msg

    def _charges(who, cases):  # cases: (claim, picked, ok(hits, msg)); keep failures
        out = []
        for claim, picked, ok in cases:
            def prove(picked=picked, ok=ok):
                hits, err, msg = _run(picked)
                return err is not None or not ok(hits, msg)
            if prove():
                out.append(_Finding(who, claim, prove))
        return out

    def _source_charges(who, cases):  # cases: (claim, passes(src)); keep failures
        out = []
        for claim, passes in cases:
            def prove(passes=passes):
                return not passes(open(__file__).read())
            if prove():
                out.append(_Finding(who, claim, prove))
        return out

    def _runtime_review():  # The Realist: executes the tool itself.
        box, other = _Body([2.0, 2.0, 3.0, 3.0, 5.0, 5.0]), _Body([2.0, 3.0, 5.0])
        tol = _Body([1.0, 1.0 * (1 + 5e-7), 1.0 * (1 + 1e-5)])
        class _ForeignFace(object):  # wrapper class the script has never seen
            def __init__(self, area, body): self.Area, self.Parent = area, body
        foreign = _Body([7.0, 7.0])
        return _charges('Realist', [
            ('box: two adjacent picks select both size-pairs, that body only',
             [box.Faces[0], box.Faces[2]],
             lambda h, m: sorted(f.Area for f in h) == [2.0, 2.0, 3.0, 3.0]
                          and m == "Selected 4 matching face(s)."),
            ('a single picked face selects exactly its size-pair',
             [box.Faces[4]], lambda h, m: sorted(f.Area for f in h) == [5.0, 5.0]),
            ('match must never cross a body boundary',
             [box.Faces[0]], lambda h, m: not any(f.Parent is other for f in h)),
            ('picks on two bodies each expand within their own body',
             [box.Faces[0], other.Faces[1]],
             lambda h, m: sorted(f.Area for f in h) == [2.0, 2.0, 2.0, 3.0, 3.0, 3.0]
                          and any(f.Parent is other for f in h)),
            ('several picks on one body expand once, never duplicated',
             [box.Faces[0], box.Faces[1], box.Faces[2]],
             lambda h, m: len(h) == 4 and len(set(id(f) for f in h)) == 4),
            ('a 5e-7 relative wobble matches, a 1e-5 wobble does not',
             [tol.Faces[0]], lambda h, m: [f.Area for f in h] == [1.0, 1.0 * (1 + 5e-7)]),
            ('faces from an unseen wrapper class are still recognized',
             [_ForeignFace(7.0, foreign)], lambda h, m: len(h) == 2),
            ('empty selection reports back and changes nothing',
             [], lambda h, m: not h and bool(m)),
        ])

    def _static_review():  # The Skeptic: reads the file's sins.
        # Needles are assembled ('ex'+'ec(') so an audit never flags its own
        # search text - the first council charged itself with exactly that.
        return _source_charges('Skeptic', [
            ('carries a SpaceClaim API-version header',
             lambda s: '# Python Script, API Version' in s),
            ('area compared against a relative, not absolute, tolerance',
             lambda s: 'AREA_TOL' in s and 'max(face.Area, other.Area)' in s),
            ('no bare except swallowing unknown errors',
             lambda s: not any(l.strip() == 'except' + ':' for l in s.splitlines())),
            ('empty selection is reported, never silent',
             lambda s: 'if not picked' in s and 'return "Select one or more' in s),
            ('faces are matched by shape, never bound to a versioned class',
             lambda s: "hasattr(x, 'Area')" in s and 'is' + 'instance(' not in s),
            ('selection goes through the version-safe ladder, not typed wrappers',
             lambda s: 'def _set_selection' in s and 'Face' + 'Selection.Create(' not in s),
            ('core logic is UI-free and returns a status string',
             lambda s: 'def expand_selection(context):' in s and 'on_click' in s),
            ('tool only fires when the SpaceClaim API exists',
             lambda s: 'if _in_spaceclaim():' in s),
            ('no eval/exec of untrusted text',
             lambda s: 'ev' + 'al(' not in s and 'ex' + 'ec(' not in s),
            ('WinForms assembly is referenced before its namespace is imported',
             lambda s: s.find('clr.AddReference') < s.find('import System.Windows.Forms')),
            ('panel carries a version beacon and closes zombie panels first',
             lambda s: 'OpenForms' in s and 'Same-Size Face Selector " + VERSION' in s),
            ('startup failure can always explain itself in the script console',
             lambda s: 'trace' + 'back' in s and 'print_exc' in s
                       and 'zombie cleanup skipped' in s),
        ])

    def _adversarial_review():  # The Surgeon: happy paths bore it; it brings knives.
        box, zero = _Body([5.0, 5.0]), _Body([0.0, 0.0])
        return _charges('Surgeon', [
            ('junk (non-face) objects in the selection are ignored',
             [object(), box.Faces[0]], lambda h, m: sorted(f.Area for f in h) == [5.0, 5.0]),
            # Junk-only input must report back; leaving the user's selection
            # untouched is correct - a crash would be auto-charged by _run.
            ('a selection of ONLY junk reports back instead of crashing',
             [object()], lambda h, m: bool(m)),
            ('a picked solid body is not treated as a face',
             [box], lambda h, m: bool(m) and 'none a face' in m),
            ('zero-area faces match each other without dividing by zero',
             [zero.Faces[0]], lambda h, m: len(h) == 2),
        ])

    def _impostor_review():  # The Impostor: impersonates SpaceClaim end-to-end.
        # Stub clr + WinForms and press the REAL panel's REAL button - the
        # interactive path is exactly what escaped two earlier councils.
        class _Form(_Control):
            instances = []
            def __init__(self):
                _Control.__init__(self)
                _Form.instances.append(self)
                self.closed = False
            def Show(self):
                wf.Application.OpenForms.append(self)
            def Close(self):
                self.closed = True
                if self in wf.Application.OpenForms:
                    wf.Application.OpenForms.remove(self)
        wf = types.ModuleType('System.Windows.Forms')
        wf.Form, wf.Label = _Form, type('Label', (_Control,), {})
        wf.Button = type('Button', (_Control,), {})
        wf.Application = type('A', (), {'OpenForms': []})
        names = ('clr', 'System', 'System.Windows', 'System.Windows.Forms')
        stubbed = dict((n, types.ModuleType(n)) for n in names)
        stubbed['clr'].AddReference = lambda *args: None
        stubbed['System'].Windows = stubbed['System.Windows']
        stubbed['System.Windows'].Forms = wf
        stubbed['System.Windows.Forms'] = wf
        saved = dict((n, sys.modules.get(n)) for n in stubbed)
        sys.modules.update(stubbed)
        box = _Body([2.0, 2.0, 3.0, 3.0, 5.0, 5.0])

        def prove(picked, ok):
            _CONTEXT.Selection = picked
            _Form.instances = []
            g = globals()
            g.update(GetActiveWindow=lambda: _Win)
            err = None
            try:
                _launch_panel()  # real launcher, fake world
                _Form.instances[-1].Controls[1].Click.fire()  # [0]=label, [1]=button
            except Exception as e:
                err = e
            finally:
                g.pop('GetActiveWindow', None)
            return (err is not None or
                    not ok(list(_CONTEXT.Selection), _Form.instances[-1].Controls[0].Text))

        cases = [
            ('run panel -> click two adjacent faces -> button grows selection',
             [box.Faces[0], box.Faces[2]],
             lambda h, msg: sorted(f.Area for f in h) == [2.0, 2.0, 3.0, 3.0]
                            and '4 matching' in msg),
            ('pressing the button with nothing picked explains, never dies',
             [], lambda h, msg: not h and 'first' in msg),
        ]
        def prove_zombie():
            stale = wf.Form(); stale.Text = 'Same-Size Face Selector v-old'; stale.Show()
            _CONTEXT.Selection = [box.Faces[4]]
            _Form.instances = []
            globals()['GetActiveWindow'] = lambda: _Win
            try:
                _launch_panel()
                _Form.instances[-1].Controls[1].Click.fire()
                err = None
            except Exception as e: err = e
            finally: globals().pop('GetActiveWindow', None)
            return (err is not None or not stale.closed
                    or sorted(f.Area for f in _CONTEXT.Selection) != [5.0, 5.0])
        out = []
        try:
            for claim, picked, ok in cases:
                if prove(picked, ok):
                    out.append(_Finding('Impostor', claim,
                                        lambda p=picked, k=ok: prove(p, k)))
            if prove_zombie():
                out.append(_Finding('Impostor', 'relaunch closes zombie panels; fresh button works', prove_zombie))
        finally:
            for name, mod in saved.items():
                if mod is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = mod
        return out

    def _minimalist_review():  # The Minimalist (AGENTS.md).
        return _source_charges('Minimalist', [
            ('file stays under 420 lines (caps: 260 tool-only, 340 +Impostor, 370+ setter ladder)',
             lambda s: len(s.splitlines()) < 420),
            ('imports stay stdlib-only plus System.*',
             lambda s: all(l.split()[1].split('.')[0] in ('sys', 'types', 'System')
                           for l in s.splitlines()
                           if l.startswith(('import ', 'from ')))),
            ('no debt markers left behind',
             lambda s: 'TO' + 'DO' not in s and 'FIX' + 'ME' not in s),
            ('the matching rule exists exactly once',
             lambda s: s.count('def same' + '_size') == 1),
            ('deliberate ceilings are marked ponytail-style',
             lambda s: 'ponytail:' in s),
        ])

    COUNCIL = [  # (name, review, ego, grudge-when-acquitted, signoff)
        ('Realist', _runtime_review, 'I ran the code itself. Opinions are not evidence.',
         'my scenarios merely chose mercy', 'It survived everything I ran. Dismissed - this once.'),
        ('Skeptic', _static_review, 'Runtime tests only prove what they ran. I read the sins.',
         'the text confessed nothing today', 'I find no sin worth the ink. Regrettably, ship it.'),
        ('Surgeon', _adversarial_review, 'Your happy paths bored me; I brought the knives.',
         'even I found no soft tissue', 'It did not bleed. I am as surprised as you are.'),
        ('Impostor', _impostor_review, 'I become SpaceClaim itself; lies do not survive me.',
         'my disguise found no seam', 'Panel, button and selection held. Allowed to live.'),
        ('Minimalist', _minimalist_review, 'Every line you write is a line I distrust.',
         'I still say it could be shorter', 'Few lines, no fat. I almost enjoyed reading it.'),
    ]

    def convene():
        print('COUNCIL IN SESSION - the accused: %s\n' % __file__)
        findings = []
        for name, review, ego, grudge, _s in COUNCIL:
            got = review()
            print('%s speaks: "%s"' % (name, ego))
            for f in got:
                print('  CHARGE: %s' % f.what)
            if not got:
                print('  brings no charge (%s).' % grudge)
            findings += got
        proven = []
        if findings:
            print('\nCross-examination (only twice-provable bugs stand):')
            for f in findings:
                if f.prove():
                    proven.append(f)
                    print('  PROVEN (%s): %s' % (f.who, f.what))
                else:
                    rival = [c[0] for c in COUNCIL if c[0] != f.who][0]
                    print('  OVERRULED by %s: %s could not prove "%s" twice.'
                          % (rival, f.who, f.what))
        if proven:
            print('\nVERDICT: GUILTY - %d bug(s) survive the council.' % len(proven))
            sys.exit(1)
        print('\nVERDICT: acquitted. Sign-offs:')
        for name, _r, _e, _g, signoff in COUNCIL:
            print('  %s: "%s"' % (name, signoff))
        print('\nOK - council adjourned: no provable bug in this file.')
        sys.exit(0)

    if __name__ == '__main__':
        convene()
