<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">

    <title>SearchBook</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
    <script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
</head>
<body>

    <header>
        <nav style="background-image: linear-gradient(90deg, rgba(189,224,237,1) 35%, rgba(243,246,250,1) 100%);" class="navbar navbar-expand-lg navbar-light bg-white shadow-sm rounded">
        </nav>
    </header>

    <main role="main" style="height:200px; background-image: linear-gradient(90deg, rgba(189,224,237,1) 35%, rgba(243,246,250,1) 100%);">
        <div class="container pt-5">
            <!-- Another variation with a button -->
            <form action="#" method="GET" onsubmit="return false">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Masukkan Kata Kunci" name="q" id="cari">
                    <div class="col-lg-1">
                        <select class="form-control" name="rank" id="rank">
                            <option value="5">5</option>
                            <option value="10">10</option>
                            <option value="20">20</option>
                            <option value="25">25</option>
                            <option value="30">30</option>
                        </select>
                    </div>
                    <div class="input-group-append">
                        <input class="btn btn-secondary fas fa-search" id="search" type="submit" value="Search">
                    </div>
                </div>
                <p>Filter Menurut :</p>
                <div class="input-group">
                    <div class="select-all">
                        <input id="all" type="checkbox" checked/>
                        <label for="all">Pilih Semua</label>
                    </div>
                    <div class="rows">
                        <input id="ahmad" type="checkbox" class="checkbox" name="type" checked/>
                        <label for="ahmad">Ahmad</label>
                    </div>
                    <div class="rows">
                        <input id="muslim" type="checkbox" class="checkbox" name="type" checked/>
                        <label for="muslim">Muslim</label>
                    </div>
                    <div class="rows">
                        <input id="ibnu-majah" type="checkbox" class="checkbox" name="type" checked/>
                        <label for="ibnu-majah">Ibnu Majah</label>
                    </div>
                    <div class="rows">
                        <input id="abu-dawud" type="checkbox" class="checkbox" name="type" checked/>
                        <label for="abu-dawud">Abu Dawud</label>
                    </div>
                    <div class="rows">
                        <input id="malik" type="checkbox" class="checkbox" name="type" checked/>
                        <label for="malik">Malik</label>
                    </div>
                    <div class="rows">
                        <input id="bukhari" type="checkbox" class="checkbox" name="type" checked/>
                        <label for="bukhari">Bukhari</label>
                    </div>
                    <div class="rows">
                        <input id="darimi" type="checkbox" class="checkbox" name="type" checked/>
                        <label for="darimi">Darimi</label>
                    </div>
                    <div class="rows">
                        <input id="nasai" type="checkbox" class="checkbox" name="type" checked/>
                        <label for="nasai">Nasai</label>
                    </div>
                    <div class="rows">
                        <input id="tirmidzi" type="checkbox" class="checkbox" name="type" checked/>
                        <label for="tirmidzi">Tirmidzi</label>
                    </div>
                </div>
            </form>
        </div>
    </main>
    <div class="row m-4" id="content">
        
        
        
    </div>
    <script>
        $(document).ready(function() {
            $(".checkbox").change(function() {
                var allChecked = $(".checkbox").length === $(".checkbox:checked").length;
                $("#all").prop("checked", allChecked);
            });
            $("#all").change(function() {
                $(".checkbox").prop("checked", this.checked);
            });
            $("#search").click(function(){
                var cari = $("#cari").val();
                var rank = $("#rank").val();
                var riwayat = [];
                $("input:checkbox[name=type]:checked").each(function() { 
                    riwayat.push($(this).attr('id'));
                }); 
                console.log(riwayat);
                $.ajax({
                    url:'/search?q='+cari+'&rank='+rank+'&riwayat='+riwayat,
                    dataType : "json",
                    success: function(data){
                        if (data.length < 1) {
                            alert("Data Tidak Ditemukan");
                            $('#content').html('<div class="row justify-content-center"><h4>Data Tidak Ditemukan</h4></div>');
                        } else {    
                            $('#content').html(data);
                        }
                    },
                    error: function(data){
                        alert("Please insert your command ");
                    }
                });
            });
        });
    </script>
</body>
</html>