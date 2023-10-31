import string
import sys
import re
import os

def get_templates(file_name):

    template_start_pattern = "^\t[A-Z].+? = \{"
    template_key_pattern = "^\t([A-Z].+?) =.+"
    template_excluded_lines = ["production_prio", "upgrade_prio"]
    template_comment_pattern = "#.+"

    template_dict = {}
    template_key = ""
    template_string = ""

    reading_template = 0
    p_count = 0
    exclude_line = 0
    exclude_p_count = 0

    file = open(file_name, 'r')
    lines = file.readlines()

    for line in lines:

        if not reading_template and re.search(template_start_pattern, line):
            exclude_template = False
            for e in excluded_template_names:
                if re.search("^.+?" + e, line):
                    exclude_template = True
                    break
            if not exclude_template:
                reading_template = True
                p_count = 0
                template_key = re.match(template_key_pattern, line).group(1)
                template_string = ""

        if reading_template:
            if not exclude_line:
                for e in template_excluded_lines:
                    if line.find(e) > -1:
                        exclude_line = True
                        exclude_p_count = 0

            if not exclude_line:
                if re.search(template_comment_pattern, line):
                    new_line = re.sub(template_comment_pattern, "", line)
                    template_string += new_line
                else:
                    template_string += line

            if exclude_line:
                exclude_p_count += line.count('{')
                exclude_p_count -= line.count('}')
                if exclude_p_count == 0:
                    exclude_line = False

            p_count += line.count('{')
            p_count -= line.count('}')

            if p_count == 0:
                reading_template = False
                template_dict[template_key] = template_string

    file.close()

    for template in template_dict:
        template_dict[template] = re.sub("\s+", " ", template_dict[template])

    return template_dict

def delete_old_target_templates(file_name):

    start_pattern = "\n" + start_text
    end_pattern = end_text + "(|\n)"

    file = open(file_name, 'r')
    contents = file.read()
    file.close()

    search_pattern = start_pattern + ".+" + "(.|\n)*?" + end_pattern + ".+"
    new_contents = re.sub(search_pattern, "", contents)

    file = open(file_name, 'w')
    file.write(new_contents)
    file.close()

def write_new_target_templates(file_name, templates):

    target_templates_title = "\n" + start_text + " (DO NOT EDIT)" + "\n\n"
    target_templates_end = "\n" + end_text + " (DO NOT EDIT)"
    target_templates_contents = ""

    for template in templates:
        new_target_template_str = text_template
        new_target_template_str = new_target_template_str.replace("<key>", template)
        new_target_template_str = new_target_template_str.replace("<template>", templates[template])
        new_target_template_str += "\n"
        target_templates_contents += new_target_template_str

    file = open(file_name, 'r')
    new_contents = file.read()
    file.close()
    
    new_contents += target_templates_title
    new_contents += target_templates_contents
    new_contents += target_templates_end

    file = open(file_name, 'w')
    file.writelines(new_contents)
    file.close()

### Main

start_text = "### Generated target template scripts"
end_text = "### End"

file = "EAI_armor_role.txt"
text_template = "<key>_target = { match_to_count = 0.96 roles = { <key>_target } upgrade_prio = { base = 0.01 }<template>}"
excluded_template_names = ["EVENT_", "EARLY_"]

def main():

    print("-Started operation")

    file_name = os.path.join(os.path.dirname(sys.argv[0]), file)
    
    delete_old_target_templates(file_name)
    target_templates = get_templates(file_name)
    write_new_target_templates(file_name, target_templates)

    print("-Finished operation")

###

if __name__ == '__main__':
    main()