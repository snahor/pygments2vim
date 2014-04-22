import os
import sys

from textwrap import dedent
from pygments.token import Token
from pygments.styles import get_style_by_name


GUI_ATTRS = ('italic', 'bold', 'underline', 'undercurl',
             'reverse', 'inverse', 'standout')

TOKENS = {
    'Token.Comment': 'Comment',  # c
    #'Token.Comment.Multiline': '',  # cm
    'Token.Comment.Preproc': 'PreProc',  # cp
    #'Token.Comment.Single': '',  # c1
    'Token.Comment.Special': 'SpecialComment',  # cs
    'Token.Error': 'Error',  # err
    #'Token.Generic': '',  # g
    'Token.Generic.Deleted': 'DiffDelete',  # gd
    #'Token.Generic.Emph': '',  # ge
    #'Token.Generic.Error': '',  # gr
    'Token.Generic.Heading': 'Title',  # gh
    'Token.Generic.Inserted': 'DiffAdd',  # gi
    #'Token.Generic.Output': '',  # go
    #'Token.Generic.Prompt': '',  # gp
    #'Token.Generic.Strong': '',  # gs
    #'Token.Generic.Subheading': '',  # gu
    #'Token.Generic.Traceback': '',  # gt
    'Token.Keyword': 'Statement',  # k
    'Token.Keyword.Constant': 'Constant',  # kc
    #'Token.Keyword.Declaration': '',  # kd
    #'Token.Keyword.Namespace': '',  # kn
    #'Token.Keyword.Pseudo': '',  # kp
    #'Token.Keyword.Reserved': '',  # kr
    'Token.Keyword.Type': 'Type',  # kt
    #'Token.Literal': '',  # l
    #'Token.Literal.Date': '',  # ld
    'Token.Literal.Number': 'Number',  # m
    'Token.Literal.Number.Float': 'Float',  # mf
    #'Token.Literal.Number.Hex': '',  # mh
    #'Token.Literal.Number.Integer': '',  # mi
    #'Token.Literal.Number.Integer.Long': '',  # il
    #'Token.Literal.Number.Oct': '',  # mo
    'Token.Literal.String': 'String',  # s
    'Token.Literal.String.Backtick': '',  # sb
    'Token.Literal.String.Char': 'Character',  # sc
    #'Token.Literal.String.Doc': '',  # sd
    'Token.Literal.String.Double': 'String',  # s2
    'Token.Literal.String.Escape': 'SpecialChar',  # se
    #'Token.Literal.String.Heredoc': '',  # sh
    #'Token.Literal.String.Interpol': '',  # si
    #'Token.Literal.String.Other': '',  # sx
    #'Token.Literal.String.Regex': '',  # sr
    'Token.Literal.String.Single': 'String',  # s1
    #'Token.Literal.String.Symbol': '',  # ss
    #'Token.Name': '',  # n
    #'Token.Name.Attribute': '',  # na
    #'Token.Name.Builtin': '',  # nb
    'Token.Name.Builtin.Pseudo': 'NonText',  # bp
    #'Token.Name.Class': '',  # nc
    'Token.Name.Constant': 'Constant',  # no
    'Token.Name.Decorator': 'pythonDecorator',  # nd
    'Token.Name.Entity': 'Special',  # ni
    'Token.Name.Exception': 'Exception',  # ne
    'Token.Name.Function': 'Function',  # nf
    'Token.Name.Label': 'Label',  # nl
    #'Token.Name.Namespace': '',  # nn
    #'Token.Name.Other': '',  # nx
    #'Token.Name.Property': '',  # py
    #'Token.Name.Tag': '',  # nt
    'Token.Name.Variable': 'Identifier',  # nv
    #'Token.Name.Variable.Class': '',  # vc
    #'Token.Name.Variable.Global': '',  # vg
    #'Token.Name.Variable.Instance': '',  # vi
    'Token.Operator': 'Operator',  # o
    #'Token.Operator.Word': '',  # ow
    #'Token.Other': '',  # x
    #'Token.Punctuation': '',  # p
    #'Token.Text': '',  #
    #'Token.Text.Whitespace': '',  # w
}


def is_color(value):
    return value.startswith('#') or ':' not in value


def convert(Style):
    lines = []
    template = (
        'hi {group:<16} guifg={guifg:<16} guibg={guibg:<16} gui={gui}'.format)

    default_foreground = (Style.styles[Token.Text] or
                          getattr(Style, 'default_style') or 'NONE')

    lines.append(template(**{
        'group': 'Normal',
        'gui': 'NONE',
        'guibg': Style.background_color or 'NONE',
        'guifg': default_foreground
    }))

    for k, v in Style.styles.iteritems():
        guibg = 'NONE'
        guifg = 'NONE'
        gui = []

        group = TOKENS.get(str(k))

        if not group:
            continue

        if not v:
            continue

        for value in v.split():
            if value in GUI_ATTRS:
                gui.append(value)
            if value.startswith('bg'):
                guibg = value[3:]
            elif is_color(value):
                guifg = value

        entry = {
            'group': group,
            'gui': ','.join(gui) or 'NONE',
            'guifg': guifg,
            'guibg': guibg
        }

        lines.append(template(**entry))

    return '\n'.join(lines)


def import_style_from_string(param):
    package_name, class_name = param.rsplit('.', 1)
    module = __import__(package_name, fromlist=[class_name])
    return getattr(module, class_name)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        output = sys.stdout
    elif len(sys.argv) == 3:
        output = open(sys.argv[2], 'wb')
    else:
        raise SystemExit('Not enough arguments')

    # try to import from pygments
    if '.' not in sys.argv[1]:
        try:
            Style = get_style_by_name(sys.argv[1].lower())
        except Exception:
            raise SystemExit('Invalid style name.')
    else:
        try:
            Style = import_style_from_string(sys.argv[1])
        except Exception:
            raise SystemExit('Could not import the style.')

    base = dedent(
        """
        " Setup {{{
        hi clear

        if exists("syntax_on")
          syntax reset
        endif

        let g:colors_name = "%s"
        " }}}
        """
    )

    with output:
        if len(sys.argv) == 3:
            output.write('" vim: sw=2 ts=2 fdm=marker\n')
            style_name = os.path.split(sys.argv[2])[1].replace('.vim', '')
            output.write(base % style_name)
            output.write('\n')
        output.write(convert(Style))
        output.write('\n')
