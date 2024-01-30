from pywinauto.application import Application
from pywinauto.timings import TimeoutError
from pywinauto.findbestmatch import MatchError
import os
import time



def start_bodyslide():
    os.startfile(r"Data\\CalienteTools\\BodySlide\\OutfitStudio x64.exe")
    app = Application().connect(path=r"Data\\CalienteTools\\BodySlide\\OutfitStudio x64.exe")
    dlg = app['Outfit Studio']
    return app, dlg

def process_bodyslide(app, dlg, shape_data_dir, project_name, pdict, mesh_directory, relative_mesh_path):
    if app is None or dlg is None:
        return app, None

    try:
        dlg.menu_select("File->New Project")
        np = app['New Project']
        np.wait('visible', timeout=10)

        np['From TemplateComboBox'].select('Convert: UNP to BHUNP')
        np['&Next >'].click()

        #here i want to change the new project name to reflect the parent folder name using relative_mesh_path
        #new_project_name = relative_mesh_path.splittext('\')[0]+project_name
        parent_folder_name = os.path.basename(os.path.dirname(relative_mesh_path))
        new_project_name = f'{parent_folder_name}_{project_name}'
        np.Edit.set_edit_text(new_project_name)

        np['From File3'].click()

        
        full_mesh_path = os.path.join(mesh_directory, relative_mesh_path)

        nifdir = os.path.join(shape_data_dir, pdict.get('sourcefile', ''))
        
        # Wait until the 'npWorkFilename' control is ready
        time.sleep(0.25)
        
        np['npWorkFilename'].Edit.set_edit_text(full_mesh_path)
        time.sleep(0.25)
        np['&Finish'].click()

        time.sleep(0.25)

        try:
            app['Target Game']['&Yes'].click()
        except (TimeoutError, MatchError):
            pass

        # Try to find the window
        window_title = f'Outfit Studio'
        dlg2 = None

        try:
            dlg2 = app[window_title]
            dlg2.wait('visible', timeout=3)
        except TimeoutError:
            # If can't find the window with the full title, try partial look
            partial_title = f'{new_project_name}'
            dlg2 = app.window(title_re=partial_title)
            dlg2.wait('visible', timeout=3)

        dlg2.menu_select("Slider->Conform All")
        time.sleep(1)

        try:
            app['Conforming...']['OK'].click()
        except (TimeoutError, MatchError):
            pass

        time.sleep(2.25)
        tb = dlg2['UNP to BHUNPEdit2']
        tb.click()
        tb.set_edit_text("100")
        tb.click()
        time.sleep(0.25)

        meshtree = dlg2['TreeView']
        meshtreeroots = meshtree.roots()
        meshtree_children = meshtreeroots[0].children()

        for child in meshtree_children:
            child.click()

            if child.text() == 'BaseShape':
                dlg2.type_keys('{DEL}')
                try:
                    app['Confirm Delete']['&Yes'].click()
                except (TimeoutError, MatchError):
                    pass
            else:
                dlg2.type_keys('{DOWN}')

        dlg2.menu_select("Slider->Set Base Shape")
        time.sleep(0.25)
        dlg2.menu_select("File->Load Reference")
        lr = app['Load Reference']
        lr['From TemplateComboBox'].select('BHUNP 3BBB Advanced Ver 4')
        lr['&OK'].click()
        dlg2.menu_select("Slider->Conform All")
        try:
            app['Conforming...']['OK'].click()
        except (TimeoutError, MatchError):
            pass

        time.sleep(2.25)
        meshtree2 = dlg2['TreeView']
        meshtreeroots2 = meshtree2.roots()
        meshtree_children2 = meshtreeroots2[0].children()

        for child in meshtree_children2:
            child.select()
            time.sleep(0.25)
            if child.text().startswith('BaseShape'):
                child.select()
                time.sleep(0.25)
                dlg2.type_keys('{DEL}')
                try:
                    app['Confirm Delete']['&Yes'].click()
                except (TimeoutError, MatchError):
                    pass
            else:
                dlg2.type_keys('{DOWN}')

        dlg2.menu_select("File->Save As")
        svas = app['Save Project As...']
        time.sleep(0.25)
        svas['Copy reference shape into outputCheckBox'].uncheck()
        time.sleep(0.25)
        svas['&Save'].click()

        return app, dlg2
    except Exception as e:
        write_to_blacklist(project_name)
        return app, None

def write_to_blacklist(project_name):
    with open('blacklist.txt', 'a') as f:
        f.write(project_name +'.nif'+ '\n')

def process_meshes(mesh_directory, shape_data_dir, pdict):
    app, dlg = start_bodyslide()
    if app is None or dlg is None:
        return

    succeeded_files = []
    failed_files = []

    if os.path.exists('failed.txt'):
        os.remove('failed.txt')

    blacklist = set()

    if os.path.exists('blacklist.txt'):
        with open('blacklist.txt', 'r') as f:
            blacklist.update(line.strip() for line in f)

    success_set = set()

    if os.path.exists('success.txt'):
        with open('success.txt', 'r') as f:
            success_set.update(line.strip() for line in f)

    for root, dirs, files in os.walk(mesh_directory):
        for file in files:
            if file.lower().endswith('_1.nif') and file not in success_set and file not in blacklist:
                project_name = os.path.splitext(file)[0]
                relative_mesh_path = os.path.relpath(os.path.join(root, file), mesh_directory)
                #print(os.path.relpath(file))
                #print(os.path.relpath(os.path.join(root, file), mesh_directory))

                try:
                    app, dlg = process_bodyslide(app, dlg, shape_data_dir, project_name, pdict, mesh_directory, relative_mesh_path)
                    if dlg is not None:
                        succeeded_files.append(file)
                        success_set.add(file)
                    else:
                        failed_files.append(file)
                except Exception as e:
                    failed_files.append(file)
                    write_to_blacklist(project_name)

    if succeeded_files:
        with open('success.txt', 'a') as f:
            f.write("\n".join(succeeded_files))

    if failed_files:
        with open('failed.txt', 'w'):
            pass

    

def main():
    basedir = 'Data\\'
    shape_data_dir = 'CalienteTools\\BodySlide\\ShapeData'
    mesh_directory = 'Data\\meshes\\'

    process_meshes(mesh_directory, shape_data_dir, {})

if __name__ == '__main__':
    main()
