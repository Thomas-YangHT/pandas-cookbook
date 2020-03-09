import * as ts from "typescript";
export declare function apply<T extends ts.Node>(node: T, ...transforms: ts.TransformerFactory<T>[]): T;
export declare function relativize_modules(relativize: (file: string, module_path: string) => string | null): (context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function import_txt(load: (txt_path: string) => string | undefined): (context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function import_css(load: (css_path: string) => string | undefined): (context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function add_init_class(): (context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function insert_class_name(): (context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function remove_use_strict(): (_context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function remove_esmodule(): (_context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function collect_deps(source: ts.SourceFile): string[];
export declare function rewrite_deps(resolve: (dep: string) => number | string | undefined): (context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function add_json_export(): (_context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function wrap_in_function(module_name: string): (_context: ts.TransformationContext) => (root: ts.SourceFile) => ts.SourceFile;
export declare function parse_es(file: string, code?: string, target?: ts.ScriptTarget): ts.SourceFile;
export declare function print_es(source: ts.SourceFile): string;
