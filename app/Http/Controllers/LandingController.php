<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class LandingController extends Controller
{
    public function search(Request $request)
    {
        $query = $request->input('q');
        $rank = $request->input('rank');
        $ind = $request->input('riwayat');

        $process = new Process(['py', "start.py", $ind, $rank, $query], 
            null,
            ['SYSTEMROOT' => getenv('SYSTEMROOT'), 'PATH' => getenv("PATH")]);
        $process->run();

        // executes after the command finishes
        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        $list_data = array_filter(explode("\n", $process->getOutput()));

        $data = array();
        $p = 1;

        // Decode each JSON result and add to data array
        foreach ($list_data as $book) {
            $dataj = json_decode($book, true);
            if (isset($dataj['score'])) {
                // Ensure the score exists before adding it
                array_push($data, $dataj);
            }
        }

        // Sort the data by score in descending order
        usort($data, function ($a, $b) {
            return $b['score'] <=> $a['score'];  // Compare score, highest first
        });

        // Limit results to the number defined by $rank
        $data = array_slice($data, 0, $rank); // Get only the first $rank items

        // Prepare the output with sorted and limited data
        $output = [];

        // Pecah query menjadi kata-kata individual
        $query_words = array_map('preg_quote', explode(' ', $query));
        $query_regex = '#' . implode('|', $query_words) . '#i';

        foreach ($data as $index => $dataj) {
            $output[] = '
            <div class="col-sm-4 py-2">
                <div class="card h-100 border-primary">
                    <div style="display: flex; flex: 1 1 auto;">
                        <div class="card-body">
                            <h6 class="card-title">Hadist Riwayat '.$dataj['riwayat'].' No. '.$dataj['number'].'</h6>
                            <p>'.substr(preg_replace($query_regex, '<span style="background-color:#FFFF66;">\\0</span>', $dataj['id']), 0,150).'...</p>
                        </div>
                    </div>
                    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModalLong'.strval($p).'">
                      Baca Selengkapnya
                    </button>

                    <div class="modal fade" id="exampleModalLong'.strval($p).'" tabindex="-1" role="dialog" aria-labelledby="exampleModalLongTitle" aria-hidden="true">
                      <div class="modal-dialog" role="document">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLongTitle">Hadist Riwayat '.$dataj['riwayat'].' No. '.$dataj['number'].'</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                              <span aria-hidden="true">&times;</span>
                            </button>
                          </div>
                          <div class="modal-body">
                            <h6>'.$dataj['arab'].'</h6>
                            <p>Artinya : '.preg_replace($query_regex, '<span style="background-color:#FFFF66;">\\0</span>', $dataj['id']).'</p>
                          </div>
                          <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Tutup</button>
                          </div>
                        </div>
                      </div>
                    </div>
                </div>
            </div>
            ';
            $p = $p + 1;
        }

        echo json_encode($output);
    }

}
