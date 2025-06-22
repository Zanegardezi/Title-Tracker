import PySimpleGUI as sg
from db import init_db, get_active_titles, get_archived_titles, mark_received, get_history
from prettytable import PrettyTable
import tempfile
import os

def titles_to_table(rows):
    if not rows:
        return [], []
    headings = list(rows[0].keys())
    data = [tuple(r) for r in rows]
    return headings, data

def main():
    init_db()
    sg.theme('LightBlue2')
    layout = [
        [sg.TabGroup([[
            sg.Tab('Active Titles', [
                [sg.Table(values=[], headings=[], key='-TABLE-', enable_events=False,
                          select_mode=sg.TABLE_SELECT_MODE_EXTENDED, auto_size_columns=True)],
                [sg.Button('Refresh'), sg.Button('Mark as Received'), sg.Button('Print Active')]
            ]),
            sg.Tab('Archived Titles', [
                [sg.Table(values=[], headings=[], key='-ARCH-', enable_events=False, auto_size_columns=True)],
                [sg.Button('Refresh Archive')]
            ]),
            sg.Tab('History', [
                [sg.Text('Stock Number:'), sg.Input(key='-HIST_SN-'), sg.Button('Load History')],
                [sg.Multiline(size=(80,20), key='-HIST_OUT-')]
            ])
        ]])]
    ]
    window = sg.Window('Title Tracker', layout, finalize=True)
    def load_active():
        rows = get_active_titles()
        headings, data = titles_to_table(rows)
        window['-TABLE-'].update(values=data, headings=headings)
    def load_archive():
        rows = get_archived_titles()
        headings, data = titles_to_table(rows)
        window['-ARCH-'].update(values=data, headings=headings)

    load_active()
    load_archive()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == 'Refresh':
            load_active()
        elif event == 'Mark as Received':
            selected_indices = values['-TABLE-']
            rows = get_active_titles()
            stock_numbers = [rows[i]['stock_number'] for i in selected_indices]
            mark_received(stock_numbers)
            load_active()
            load_archive()
        elif event == 'Print Active':
            rows = get_active_titles()
            pt = PrettyTable()
            if rows:
                pt.field_names = list(rows[0].keys())
                for r in rows:
                    pt.add_row(r)
            temp = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            temp.write(str(pt).encode())
            temp.close()
            os.startfile(temp.name, 'print')
        elif event == 'Refresh Archive':
            load_archive()
        elif event == 'Load History':
            sn = values['-HIST_SN-']
            hist = get_history(sn)
            text = '\n'.join([f"{h['timestamp']}: {h['old_status']} → {h['new_status']}" for h in hist])
            window['-HIST_OUT-'].update(text)
    window.close()

if __name__=='__main__':
    main()
