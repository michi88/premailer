import sys
import argparse

from premailer import Premailer


def main(args):
    """Command-line tool to transform html style to inline css

    Usage::

        $ echo '<style>h1 { color:red; }</style><h1>Title</h1>' | python -m premailer
        <h1 style="color:red"></h1>
        $ cat newsletter.html | python -m premailer
    """

    parser = argparse.ArgumentParser(usage='python -m premailer [options]')

    parser.add_argument(
        "-f", "--file", nargs='?', type=argparse.FileType('r'),
        help="Specifies the input file.  The default is stdin.",
        default=sys.stdin, dest="infile"
    )

    parser.add_argument(
        "-o", "--output", nargs='?', type=argparse.FileType('w'),
        help="Specifies the output file.  The default is stdout.",
        default=sys.stdout, dest="outfile"
    )

    parser.add_argument(
        "--base-url", default=None, type=str, dest="base_url"
    )

    parser.add_argument(
        "--remove-internal-links", default=True,
        help="Remove links that start with a '#' like anchors.",
        dest="preserve_internal_links"
    )

    parser.add_argument(
        "--exclude-pseudoclasses", default=False,
        help="Pseudo classes like p:last-child', p:first-child, etc",
        action="store_true", dest="exclude_pseudoclasses"
    )

    parser.add_argument(
        "--preserve-style-tags", default=False,
        help="Do not delete <style></style> tags from the html document.",
        action="store_true", dest="keep_style_tags"
    )

    parser.add_argument(
        "--keep-original-css", default=False,
        help="Never remove or strip any of the original css found in the original head of the document.",
        action="store_true", dest="keep_original_css"
    )

    parser.add_argument(
        "--remove-star-selectors", default=True,
        help="All wildcard selectors like '* {color: black}' will be removed.",
        action="store_false", dest="include_star_selectors"
    )

    parser.add_argument(
        "--remove-classes", default=False,
        help="Remove all class attributes from all elements",
        action="store_true", dest="remove_classes"
    )

    parser.add_argument(
        "--strip-important", default=False,
        help="Remove '!important' for all css declarations.",
        action="store_true", dest="strip_important"
    )

    parser.add_argument(
        "--method", default="html", dest="method",
        help="The type of html to output. 'html' for HTML, 'xml' for XHTML."
    )

    parser.add_argument(
        "--base-path", default=None, dest="base_path",
        help="The base path for all external stylsheets."
    )

    parser.add_argument(
        "--external-style", action="append", dest="external_styles",
        help="The path to an external stylesheet to be loaded."
    )
    parser.add_argument(
        "--disable-basic-attributes", dest="disable_basic_attributes",
        help="Disable provided basic attributes (comma separated)", default=[]
    )

    parser.add_argument(
        "--disable-validation", default=False,
        action="store_true", dest="disable_validation",
        help="Disable CSSParser validation of attributes and values",
    )

    options = parser.parse_args(args)

    if options.disable_basic_attributes:
        options.disable_basic_attributes = options.disable_basic_attributes.split()

    p = Premailer(
        html=options.infile.read().decode('utf-8'),
        base_url=options.base_url,
        preserve_internal_links=options.preserve_internal_links,
        exclude_pseudoclasses=options.exclude_pseudoclasses,
        keep_style_tags=options.keep_style_tags,
        keep_original_css=options.keep_original_css,
        include_star_selectors=options.include_star_selectors,
        remove_classes=options.remove_classes,
        strip_important=options.strip_important,
        external_styles=options.external_styles,
        method=options.method,
        base_path=options.base_path,
        disable_basic_attributes=options.disable_basic_attributes,
        disable_validation=options.disable_validation
    )
    options.outfile.write(p.transform())
    return 0


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
